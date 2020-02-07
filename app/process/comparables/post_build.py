from app.utils.move_backups import copy_backups
from app.settings import envs


def copy_raw_comps(version):
    copy_backups(
        remote_server=envs.LON_SQL_04,
        backup_regex=envs.RAW_COMPS_REGEX.format(version_number=version),
        source_directory=envs.LON_SQL_04_DB_BACKUPS,
        target_directory=envs.LON_SQL_01_RAW_COMPS_BACKUPS
    )


def copy_comps(version):
    copy_backups(
        remote_server=envs.LON_SQL_04,
        backup_regex=envs.COMPS_REGEX.format(version_number=version),
        source_directory=envs.LON_SQL_04_DB_BACKUPS,
        target_directory=envs.LON_SQL_01_COMPS_BACKUPS
    )


def move_backups(version):
    copy_raw_comps(version)
    copy_comps(version)


if __name__ == '__main__':
    move_backups(688)
