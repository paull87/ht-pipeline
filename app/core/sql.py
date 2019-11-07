import sqlalchemy
import pandas
from contextlib import contextmanager
from app.settings.envs import LON_SQL_03, LON_SQL_02_SQLCEN

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
        try:
            connection = self.engine.connect()
            yield connection
        finally:
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

    def execute(self, sql_query):
        with self.connection.connect() as conn:
            return self._executor(con=conn, sql=sql_query)


def lon_sql_03_runner():
    connection = SQLConnection('sqlserver', LON_SQL_03, 'master')
    return SQLQueryRunner(connection)


def lon_sql_02_sqlcen_runner():
    connection = SQLConnection('sqlserver', LON_SQL_02_SQLCEN, 'master')
    return SQLQueryRunner(connection)


if __name__ == '__main__':
    from app.settings.envs import LON_SQL_02_SQLCEN
    odbc = 'sqlserver'
    database = 'GDW3'
    test_connection = SQLConnection(odbc, LON_SQL_02_SQLCEN, database)
    query_runner = SQLQueryRunner(test_connection)

    query = 'SELECT * FROM [GDW3].[dbo].[tab_buildManifest]'
    result = query_runner.read(query)

    print(result)