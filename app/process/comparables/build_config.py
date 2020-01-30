import os
from app.core.sql import get_sql_runner
from app.settings.envs import ADHOC_FILE_PATH


LON_SQL_04_SQL_RUNNER = get_sql_runner('lon-sql-04')
LON_SQL_02_SQL_RUNNER = get_sql_runner('lon-sql-02')
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



def get_bulk_test_id(version, bulk_test_type):
    """Returns the latest bulk test id for the given version and bulk test type."""
    result = LON_SQL_02_SQL_RUNNER.read(bulk_test_id_sql.format(version=version, bulk_test_type=bulk_test_type))
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


def get_bulk_test_ids(current_version, compare_version):
    return {
        'primary_client': secondary_client(current_version),
        'primary_capital': secondary_capital(current_version),
        'primary_rental': secondary_rental(current_version),
        'primary_rental_client': secondary_rental_client(current_version),
        'secondary_client': secondary_client(compare_version),
        'secondary_capital': secondary_capital(compare_version),
        'secondary_rental': secondary_rental(compare_version),
        'secondary_rental_client': secondary_rental_client(compare_version),
    }


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
