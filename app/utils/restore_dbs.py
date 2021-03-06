from app.core.sql import get_sql_runner
from app.utils.move_backups import get_latest_backup, copy_backups, delete_backups
from app.settings.envs import BACKUP_DIRS, BACKUP_REGEXS, SERVERS
import os
import argparse


def restore_db(server, database, database_name, version, copy_file_from=None):
    backup_directory = BACKUP_DIRS[server][database]
    backup_regex = BACKUP_REGEXS[database]
    if copy_file_from:
        copy_backups(
            remote_server=SERVERS[server],
            backup_regex=backup_regex.format(version_number=version),
            source_directory=BACKUP_DIRS[copy_file_from][database],
            target_directory=backup_directory
        )
    backup_file_name = get_latest_backup(
        server=server,
        source_directory=backup_directory,
        file_regex=backup_regex.format(version_number=version),
    )
    full_backup_path = os.path.join(backup_directory, backup_file_name)
    sql_runner = get_sql_runner(server)
    sql_runner.restore_db(database_name, full_backup_path)
    if copy_file_from:
        delete_backups(
            remote_server=SERVERS[server],
            backup_file=full_backup_path,
        )


if __name__ == '__main__':
    #restore_db('dev-sql-01', 'gdw', 'GDW3', 227)
    #restore_db('lon-sql-03', 'comps', 'Comparables', 679, copy_file_from='lon-sql-01')
    #restore_db('lon-sql-02', 'raw_comps', 'rawComparables', 679, copy_file_from='lon-sql-01')
    #restore_db('lon-sql-02', 'gdw', 'GDW3', 227, copy_file_from='lon-sql-01')
    #restore_db('lon-sql-02', 'nhbc', 'NHBC', 209, copy_file_from='lon-sql-01')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s',
        '--server',
        dest='server',
        help='Server to restore db to',
        required=True,
    )
    parser.add_argument(
        '-d',
        '--database',
        dest='database',
        help='Database to restore',
        required=False
    )

    parser.add_argument(
        '-n',
        '--database_name',
        dest='database_name',
        help='Name to restore database as',
        required=True
    )

    parser.add_argument(
        '-v',
        '--version',
        dest='version',
        help='Version of database to restore',
        required=True
    )

    parser.add_argument(
        '-c',
        '--copy_file_from',
        dest='copy_file_from',
        help='Source server where the backup needs copying from',
        required=False
    )

    args = parser.parse_args()
    restore_db(**vars(args))
