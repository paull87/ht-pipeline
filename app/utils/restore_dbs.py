from app.core.sql import get_sql_runner
from app.utils.move_backups import get_latest_backup, copy_backups
from app.settings.envs import BACKUP_DIRS, BACKUP_REGEXS, SERVERS
import os


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


if __name__ == '__main__':
    restore_db('dev-sql-01', 'raw_comps', 'PL_TEST_raw_comps', 679)
    #restore_db('lon-sql-03', 'comps', 'Comparables', 679, copy_file_from='lon-sql-01')
