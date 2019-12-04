import re
import os
from app.core.remote_windows import RemoteSession
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
    remote_lon_sql_04 = RemoteSession(envs.LON_SQL_04, (secrets.USER_NAME, secrets.PASSWORD))

    print(remote_lon_sql_04.ls(envs.LON_SQL_04_DB_BACKUPS))

    raw_comps_regex = envs.RAW_COMPS_REGEX.format(version_number=678)

    print(list(find_backups(raw_comps_regex, remote_lon_sql_04.ls(envs.LON_SQL_04_DB_BACKUPS))))

    #copy_backups(remote_lon_sql_04, raw_comps_regex, envs.LON_SQL_04_DB_BACKUPS, envs.LON_SQL_01_RAW_COMPS_BACKUPS)
