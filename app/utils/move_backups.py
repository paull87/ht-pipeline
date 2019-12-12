import re
import os
from app.core.remote_windows import RemoteSession
from app.settings import envs, secrets
from app.core.logger import logger


def copy_backups(remote_server, backup_regex, source_directory, target_directory):
    session = RemoteSession(remote_server, (secrets.USER_NAME, secrets.PASSWORD))
    files = session.ls(source_directory)
    for file in find_backups(backup_regex, files):
        logger.info(f'Copying file {file} to {target_directory}')
        session.copy(
            source_file=os.path.join(source_directory, file),
            destination=target_directory,
        )


def find_backups(file_regex, files):
    for file in files:
        if re.search(file_regex, file):
            yield file


def get_latest_backup(server, source_directory, file_regex):
    session = RemoteSession(server, (secrets.USER_NAME, secrets.PASSWORD))
    backups = session.ls(source_directory)
    version_backups = list(find_backups(file_regex, backups))
    if len(version_backups) == 0:
        logger.error(f'No backup found matching {file_regex}')
        raise Exception(f'No backup found matching {file_regex}')
    backup_file = version_backups[-1]
    logger.info(f'Found backup {backup_file}')
    return backup_file


if __name__ == '__main__':
    raw_comps_regex = envs.RAW_COMPS_REGEX.format(version_number=678)

    copy_backups(
        remote_server=envs.LON_SQL_04,
        backup_regex=raw_comps_regex,
        source_directory=envs.LON_SQL_01_RAW_COMPS_BACKUPS,
        target_directory=envs.LON_SQL_04_DB_BACKUPS
    )
