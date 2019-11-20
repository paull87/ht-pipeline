import re
import os
from app.core.remote_windows import RemoteWindow
from app.settings import envs, secrets


def copy_backups(remote_server, backup_regex, source_directory, target_directory):
    files = remote_server.ls(envs.LON_SQL_04_DB_BACKUPS)
    for file in find_backups(backup_regex, files):
        remote_server.copy(
            target=os.path.join(source_directory, file),
            destination=target_directory,
        )


def find_backups(file_regex, files):
    for file in files:
        if re.search(file_regex, file):
            yield file


if __name__ == '__main__':
    raw_comps_regex = r'^rawComparables_.+_\d\d\d\d_\d\d_\d\d.bak$'
    remote_lon_sql_04 = RemoteWindow(envs.LON_SQL_04, (secrets.USER_NAME, secrets.PASSWORD))

    print(remote_lon_sql_04.ls(envs.LON_SQL_01_RAW_COMPS_BACKUPS))

    #copy_backups(remote_lon_sql_04, raw_comps_regex, envs.LON_SQL_04_DB_BACKUPS, envs.LON_SQL_01_RAW_COMPS_BACKUPS)
