import sqlalchemy
import pandas
import threading
import datetime
import os
import time
from contextlib import contextmanager
from app.settings.envs import SERVERS
from app.core.logger import logger

connection_strings = {
    'sqlserver': 'mssql+pyodbc://{server_name}/{db_name}?driver=SQL+Server'
}


class SQLConnection:
    def __init__(self, odbc, server, database):
        self.odbc = odbc
        self.server = server
        self.database = database
        self.engine = self.create_engine()
        self._connection = None

    @contextmanager
    def connect(self):
        connection = None
        try:
            connection = self.engine.connect()
            yield connection
        except Exception as e:
            logger.error(f'Unable to connect to {self.server}: e')
            raise e
        finally:
            if connection:
                connection.close()

    @contextmanager
    def raw_connect(self):
        connection = None
        try:
            connection = self.engine.raw_connection()
            yield connection
        except Exception as e:
            logger.error(f'Unable to connect to {self.server}: e')
            raise e
        finally:
            if connection:
                connection.close()

    def create_engine(self):
        conn_string = connection_strings[self.odbc]
        return sqlalchemy.create_engine(conn_string.format(server_name=self.server, db_name=self.database))


class SQLQueryRunner:
    def __init__(self, connection):
        self._executor = pandas.io.sql.execute
        self._reader = pandas.io.sql.read_sql
        self.connection = connection

    def read(self, sql_query):
        with self.connection.connect() as conn:
            return self._reader(con=conn, sql=sql_query)

    def execute(self, sql_query, wait_delay=0):
        with self.connection.connect() as conn:
            self._executor(con=conn, sql=sql_query)
            time.sleep(wait_delay)

    def restore(self, query):
        """
        Restores require a cursor in order to keep the connection alive for the
        entirety of the restore operation.
        """
        with self.connection.raw_connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            while cursor.nextset():
                pass

    def restore_db(self, database, backup_file, stats=5):
        restore_query = self.restore_database_query(database, backup_file)
        logger.info(f'Running restore query:\n{restore_query}')
        restore_thread = threading.Thread(target=self.restore, args=(restore_query,))
        restore_thread.start()
        percent_complete = 0
        while restore_thread.is_alive():
            if percent_complete == 100:
                logger.info(f'{database} restore finalising')
            restore_state = self.get_restore_state(database)
            if not restore_state:
                percent_complete = 100
                continue
            current_percent_complete = restore_state.percent_complete
            seconds_to_complete = restore_state.seconds_to_complete
            current_percent_complete = current_percent_complete - (current_percent_complete % stats)
            if current_percent_complete > percent_complete:
                percent_complete = current_percent_complete
                expected_finish = datetime.datetime.now() + datetime.timedelta(seconds=seconds_to_complete)
                logger.info(f'{database} restored {percent_complete}: expected finish {expected_finish}')
            time.sleep(5)
        logger.info(f'{database} restore complete')

    def get_restore_state(self, database):
        sql_query = f'''
        SELECT 
            percent_complete,
            estimated_completion_time/1000 AS seconds_to_complete
        FROM sys.dm_exec_requests r CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) a
        WHERE r.command in ('RESTORE DATABASE')
        AND a.text LIKE '%{database}%';
        '''
        restore = self.read(sql_query)
        try:
            return next(restore.itertuples())
        except StopIteration:
            return

    @property
    def default_data_path(self):
        sql_query = '''
            SELECT CAST(SERVERPROPERTY('InstanceDefaultDataPath') AS NVARCHAR(4000)) AS DataPath;
        '''
        result = self.read(sql_query)
        return result.loc[0, 'DataPath']

    @property
    def default_log_path(self):
        sql_query = '''
                SELECT CAST(SERVERPROPERTY('InstanceDefaultLogPath') AS NVARCHAR(4000)) AS LogPath;
            '''
        result = self.read(sql_query)
        return result.loc[0, 'LogPath']

    def get_backup_filelist(self, backup_file):
        sql_query = f'''
            RESTORE FILELISTONLY 
            FROM DISK = N'{backup_file}';  
        '''
        result = self.read(sql_query)
        return list(result.itertuples())

    def restore_database_query(self, database, backup_file):
        file_list = self._format_restore_file_move(backup_file)
        return f'''
            RESTORE DATABASE [{database}] 
            FROM DISK = N'{backup_file}' WITH FILE = 1,  
            {file_list},  
            NOUNLOAD,  
            REPLACE,
            RECOVERY;
        '''

    def list_databases(self):
        sql_query = '''
            SELECT [name]
            FROM sys.databases
            WHERE database_id > 4;
        '''
        result = self.read(sql_query)
        return result['name'].values

    def drop_database(self, database_name):
        sql_query = f'DROP DATABASE {database_name};'
        # TODO: Add sql runner call
        print(sql_query)
        logger.info(f'Dropping database {database_name} on server {self.connection.server}')

    def _default_path_for_file(self, file_type):
        if file_type == 'L':
            return self.default_log_path
        else:
            return self.default_data_path

    def _format_restore_file_move(self, backup_file):
        files = []
        move_fmt = "MOVE N'{logical_name}' TO N'{file_name}'"
        for file in self.get_backup_filelist(backup_file):
            file_name = os.path.basename(file.PhysicalName)
            file_directory = self._default_path_for_file(file.Type)
            files.append(
                move_fmt.format(
                    logical_name=file.LogicalName,
                    file_name=os.path.join(file_directory, file_name)
                )
            )
        return ','.join(files)


def get_sql_runner(server):
    server_name = SERVERS[server]
    connection = SQLConnection('sqlserver', server_name, 'master')
    return SQLQueryRunner(connection)


if __name__ == '__main__':
    sql_runner = get_sql_runner('lon-sql-04')
    print(sql_runner.list_databases())
