from app.core.logger import logger
from app.core.slack_client import send_message
from app.core.sql import get_sql_runner
from app.core.remote_windows import RemoteSession
from app.process.comparables.build_config import current_config, delete_config, CONFIG_FILE

from xml.etree import ElementTree

comps_server = 'lon-sql-04'
lon_sql_02 = 'lon-sql-02'

LON_SQL_04_SQL_RUNNER = get_sql_runner(comps_server)
LON_SQL_02_SQL_RUNNER = get_sql_runner(lon_sql_02)
LON_SQL_02_SESSION = RemoteSession(lon_sql_02)


run_build_sql = '''
EXEC buildManager.dbo.proc_runBuildManager
      @buildTypeID = {build_type_id}
    , @buildControllerId = {build_controller_id}
    , @buildJobName = '{build_job_name}'
    , @buildDescription = '{build_description}'
    , @buildConfiguration = '{build_config}'
    , @isReleaseBuild = {is_release_build};
'''

BUILD_TYPE_ID = 1
BUILD_CONTROLLER_ID = 24
BUILD_JOB_NAME = '1_comparablesBuildController.dtsx'


def drop_raw_comps_databases():
    for database in LON_SQL_04_SQL_RUNNER.list_databases():
        if database.startswith('rawComparables_'):
            LON_SQL_04_SQL_RUNNER.drop_database(database)


def comps_to_delete(comps_database, versions_to_keep):
    for version in versions_to_keep:
        if comps_database.endswith(str(version)):
            return False
    return True


def drop_comps_databases(versions_to_keep):
    for database in get_comps_databases():
        if comps_to_delete(database, versions_to_keep):
            LON_SQL_04_SQL_RUNNER.drop_database(database)


def get_comps_databases():
    return [d for d in LON_SQL_04_SQL_RUNNER.list_databases() if d.startswith('Comparables_')]


def latest_comps_build_version():
    query = '''
        SELECT TOP 1 buildVersionNumber
        FROM buildManager.dbo.tab_build
        ORDER BY 1 DESC;
    '''
    result = LON_SQL_02_SQL_RUNNER.read(query)
    return result.loc[0, 'buildVersionNumber']


def parse_config():
    config = ElementTree.parse(CONFIG_FILE).getroot()
    return {c.tag: c.text for c in config.getchildren()}


def config_based_on_version():
    return parse_config().get('basedOnBuildVersionNumber')


def config_compare_to_version():
    return parse_config().get('compareToBuildVersionNumber')


def prepare_build():
    """
    Clears out the old databases to free space for the new build.
    """
    drop_raw_comps_databases()
    drop_comps_databases(
        (config_based_on_version(), config_compare_to_version())
    )


def start_build(sql):
    sql = sql.replace('\n', ' ')
    cmd = f'sqlcmd -S {LON_SQL_02_SQL_RUNNER.connection.server} -Q "{sql}"'
    LON_SQL_02_SESSION.run_cmd(cmd)
    return latest_comps_build_version()


def run_build(sql):
    current_build_version = start_build(sql)
    monitor_build(current_build_version)


def monitor_build(current_build_version=None):
    current_build_version = current_build_version or latest_comps_build_version()
    send_message('#ht-compsbuild', f'Started Comps Build {current_build_version}')
    try:
        op_id = LON_SQL_04_SQL_RUNNER.latest_package_operation_id(BUILD_JOB_NAME)
        LON_SQL_04_SQL_RUNNER.monitor_package_status(op_id)
        logger.info(f'Comps Build {current_build_version} complete.')
        send_message('#ht-compsbuild', f'Comps Build {current_build_version} completed successfully!')
    except Exception as e:
        logger.error(f'Comps Build {current_build_version} failed.\n{e}')
        send_message('#ht-compsbuild', f'Comps Build {current_build_version} failed.\n{e}')


def run(build_description, is_release_build, dry_run=False):
    sql = run_build_sql.format(
        build_type_id=BUILD_TYPE_ID,
        build_controller_id=BUILD_CONTROLLER_ID,
        build_job_name=BUILD_JOB_NAME,
        build_description=build_description,
        build_config=current_config(),
        is_release_build=int(is_release_build),
    )
    if dry_run:
        print(sql)
    else:
        prepare_build()
        run_build(sql)
