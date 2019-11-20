import os
import datetime
import argparse
from app.core.sql import lon_sql_02_sqlcen_runner
from app.settings.envs import ADHOC_FILE_PATH

# Used as default if no month  is passed to the process
current_month = datetime.datetime.now().strftime('%Y%m%d')

CONFIG_FILE = os.path.join(ADHOC_FILE_PATH, 'comps_build_config')

CONFIG_TEMPLATE = '''<buildConfiguration>
 <ticketNumber />
 <asOfDate>{as_of_date}</asOfDate>
 <basedOnBuildVersionNumber>{based_on_version}</basedOnBuildVersionNumber>
 <compareToBuildVersionNumber>{compared_to_version}</compareToBuildVersionNumber>
 <bulkTestAVMType>hybrid</bulkTestAVMType>
 <releaseDate />
 <basedOnOSVersion>{os_version}</basedOnOSVersion>
 <bulkTestIdSecondaryCapital>{secondary_capital}</bulkTestIdSecondaryCapital>
 <bulkTestIdSecondaryRental>{secondary_rental}</bulkTestIdSecondaryRental>
 <bulkTestIdSecondaryClient>{secondary_client}</bulkTestIdSecondaryClient>
 <bulkTestIdSecondaryCapitalInCycle />
 <bulkTestIdSecondaryRentalClient>{secondary_rental_client}</bulkTestIdSecondaryRentalClient>
 <rebuildCandidate>{rebuild}</rebuildCandidate>
 <updateCandidate>{update}</updateCandidate>
 <generateGeoService>{geo_service}</generateGeoService>
</buildConfiguration>'''

bulk_test_id_sql = '''
SELECT TOP 1 bulkTestId
FROM bulktestmanager.realtime.vw_bulkTestDetails
WHERE
    buildversionnumber = {version}
    AND bulkTestType = '{bulk_test_type}'
ORDER BY
    bulktestTypeID,
    bulktestdatetime desc;'''

BUILD_TYPE_ID = 1
BUILD_CONTROLLER_ID = 24
BUILD_JOB_NAME = 'runProductionComparablesBuildxx'

run_build_sql = '''
USE buildManager;
GO
EXEC dbo.proc_runBuildManager
      @buildTypeID = {build_type_id}
    , @buildControllerId = {build_controller_id}
    , @buildJobName = '{build_job_name}'
    , @buildDescription = '{build_description}'
    , @buildConfiguration = '{build_config}'
    , @isReleaseBuild = {is_release_build};
'''


def str_to_bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_bulk_test_id(version, bulk_test_type):
    """Returns the latest bulk test id for the given version and bulk test type."""
    result = lon_sql_02_sqlcen_runner().read(bulk_test_id_sql.format(version=version, bulk_test_type=bulk_test_type))
    if not result.empty:
        return result.loc[0, 'bulkTestId']


def secondary_capital(version_number):
    """Returns the latest capital bulk test id for the given version."""
    return get_bulk_test_id(version_number, 'Capital')


def secondary_rental(version_number):
    """Returns the latest rental bulk test id for the given version."""
    return get_bulk_test_id(version_number, 'Rental')


def secondary_client(version_number):
    """Returns the latest client bulk test id for the given version."""
    return get_bulk_test_id(version_number, 'HybridClient')


def secondary_rental_client(version_number):
    """Returns the latest rental client bulk test id for the given version."""
    return get_bulk_test_id(version_number, 'RentalClient')


def build_config(as_of_date, os_version, based_on_version, compared_to_version, rebuild, update, geo_service):
    config = CONFIG_TEMPLATE.format(
        as_of_date=as_of_date,
        os_version=os_version,
        based_on_version=based_on_version,
        compared_to_version=compared_to_version,
        secondary_capital=secondary_capital(compared_to_version),
        secondary_rental=secondary_rental(compared_to_version),
        secondary_client=secondary_client(compared_to_version),
        secondary_rental_client=secondary_rental_client(compared_to_version),
        rebuild=int(rebuild),
        update=int(update),
        geo_service=int(geo_service),
    )
    with open(CONFIG_FILE, 'w') as file:
        file.write(config)

    print(config)


def current_config():
    """Returns the current saved config file as found in CONFIG_FILE."""
    try:
        with open(CONFIG_FILE, 'r') as file:
            return file.read()
    except FileNotFoundError:
        raise Exception('Config has not been generated yet. Please run build_config first.')


def show_config():
    print(current_config())


def delete_config():
    """Deletes the current config file if it exists."""
    if os.path.isfile(CONFIG_FILE):
        os.remove(CONFIG_FILE)


def run_build(build_description, is_release_build, dry_run=False):
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
        #TODO: add sql run
        # Delete the config so it can't be accidentally used again.
        delete_config()


def process_action(
        action,
        as_of_date,
        os_version,
        based_on_version,
        compared_to_version,
        rebuild,
        update,
        geo_service,
        build_description,
        is_release_build,
):
    if action == 'build':
        build_config(as_of_date, os_version, based_on_version, compared_to_version, rebuild, update, geo_service )
    elif action == 'show':
        show_config()
    elif action == 'run':
        run_build(build_description, is_release_build)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a',
        '--action',
        dest='action',
        help='Action to build config, show config, or run comps config',
        required=True,
        choices=['build', 'show', 'run'],
    )
    parser.add_argument(
        '-as',
        '--asof',
        dest='as_of_date',
        default=current_month,
        help='As of date for the config',
        required=False
    )

    parser.add_argument(
        '-o',
        '--os_version',
        dest='os_version',
        help='OS data version to use for the config',
        required=False
    )

    parser.add_argument(
        '-b',
        '--based_on_version',
        dest='based_on_version',
        help='Comps version based on to use for the config',
        required=False
    )

    parser.add_argument(
        '-c',
        '--compared_to_version',
        dest='compared_to_version',
        help='Comps version compared to to use for the config',
        required=False
    )

    parser.add_argument(
        '-r',
        '--rebuild',
        dest='rebuild',
        type=str_to_bool,
        help='Whether comps build is rebuild or not',
        required=False
    )

    parser.add_argument(
        '-u',
        '--update',
        dest='update',
        type=str_to_bool,
        help='Whether comps build is update or not',
        required=False
    )

    parser.add_argument(
        '-g',
        '--geo_service',
        dest='geo_service',
        type=str_to_bool,
        help='Whether comps build requires a geo service update',
        required=False
    )

    parser.add_argument(
        '-d',
        '--description',
        dest='build_description',
        help='Build description',
        required=False
    )

    parser.add_argument(
        '-i',
        '--is_release_build',
        dest='is_release_build',
        type=str_to_bool,
        help='Whether comps build is release build or not',
        required=False
    )

    args = parser.parse_args()
    process_action(**vars(args))
