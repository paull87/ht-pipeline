import os

# Servers
DEV_SQL_01 = 'DEV-SQL-01\SQLDEV'
DEV_APP_01 = 'DEV-APP-01'
LON_SQL_01 = 'LON-SQL-01'
LON_SQL_01_SOURCEBUILD = 'LON-SQL-01\SOURCEBUILD'
LON_SQL_02_SQLCEN = r'LON-SQL-02\SQLCEN'
LON_SQL_03 = 'LON-SQL-03'
LON_SQL_04 = 'LON-SQL-04'
LON_SQL_10 = 'LON-SQL-10'
LON_DWN_01 = 'LON_DWN_01'
LON_SQL_06 = 'LON-SQL-06'
LON_SQL_06_GEOINDEXAPP = r'LON-SQL-06\GeoindexApp'

SERVERS = {
    'dev-sql-01': DEV_SQL_01,
    'dev-app-01': DEV_APP_01,
    'lon-dwn-01': LON_DWN_01,
    'lon-sql-01': LON_SQL_01,
    'lon-sql-02': LON_SQL_02_SQLCEN,
    'lon-sql-03': LON_SQL_03,
    'lon-sql-04': LON_SQL_04,
    'lon-sql-06': LON_SQL_06_GEOINDEXAPP,
    'lon-sql-10': LON_SQL_10,
}

ADHOC_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'adhoc_files')

DATA_ENGINEERING_CHANNEL = '#ht-data-engineers'


# Backup File Directories
LON_SQL_04_DB_BACKUPS = 'D:\MSSQL\BACKUP'
LON_SQL_06_DB_BACKUPS = 'E:\MSSQL\Backup'
LON_SQL_03_DB_BACKUPS = 'D:\BACKUP'
LON_SQL_02_DB_BACKUPS = 'E:\MSSQL\Backup'

LON_SQL_01_RAW_COMPS_BACKUPS = r'\\lon-sql-01\DBRepository\rawComparables\2019'
LON_SQL_01_COMPS_BACKUPS = r'\\lon-sql-01\DBRepository\comparables\2019'
LON_SQL_01_NHBC_BACKUPS = r'\\lon-sql-01\DBRepository\nhbc'
LON_SQL_01_OS_DATA_BACKUPS = r'\\lon-sql-01\DBRepository\os_data\2019'
LON_SQL_01_GDW_BACKUPS = r'\\lon-sql-01\DBRepository\gdw3'

BACKUP_DIRS = {
    'lon-sql-01': {
        'nhbc': LON_SQL_01_NHBC_BACKUPS,
        'raw_comps': LON_SQL_01_RAW_COMPS_BACKUPS,
        'comps': LON_SQL_01_COMPS_BACKUPS,
        'os_data': LON_SQL_01_OS_DATA_BACKUPS,
        'gdw': LON_SQL_01_GDW_BACKUPS,
    },
    'dev-sql-01': {
        'nhbc': LON_SQL_01_NHBC_BACKUPS,
        'raw_comps': LON_SQL_01_RAW_COMPS_BACKUPS,
        'comps': LON_SQL_01_COMPS_BACKUPS,
        'os_data': LON_SQL_01_OS_DATA_BACKUPS,
        'gdw': LON_SQL_01_GDW_BACKUPS,
    },
    'dev-app-01': {
        'nhbc': LON_SQL_01_NHBC_BACKUPS,
        'raw_comps': LON_SQL_01_RAW_COMPS_BACKUPS,
        'comps': LON_SQL_01_COMPS_BACKUPS,
        'os_data': LON_SQL_01_OS_DATA_BACKUPS,
        'gdw': LON_SQL_01_GDW_BACKUPS,
    },
    'lon-sql-06': {
        'nhbc': LON_SQL_06_DB_BACKUPS,
        'raw_comps': LON_SQL_06_DB_BACKUPS,
        'comps': LON_SQL_06_DB_BACKUPS,
        'os_data': LON_SQL_06_DB_BACKUPS,
    },
    'lon-sql-03': {
        'nhbc': LON_SQL_03_DB_BACKUPS,
        'raw_comps': LON_SQL_03_DB_BACKUPS,
        'comps': LON_SQL_03_DB_BACKUPS,
        'os_data': LON_SQL_03_DB_BACKUPS,
    },
    'lon-sql-02': {
        'nhbc': LON_SQL_02_DB_BACKUPS,
        'raw_comps': LON_SQL_02_DB_BACKUPS,
        'comps': LON_SQL_02_DB_BACKUPS,
        'os_data': LON_SQL_02_DB_BACKUPS,
        'gdw': LON_SQL_02_DB_BACKUPS,
    }
}

RAW_COMPS_REGEX = r'^rawComparables_v?{version_number}_\d\d\d\d_\d+_\d+.bak$'
NHBC_REGEX = r'^NHBC_v?{version_number}.bak$'
OS_DATA_REGEX = r'^OS_Data_v?{version_number}.bak$'
COMPS_REGEX = r'LON-SQL-04_Comparables_v?{version_number}_\d\d\d\d_\d+_\d+.bak'
GDW_REGEX = r'^GDW3_v?{version_number}.bak$'

BACKUP_REGEXS = {
    'nhbc': NHBC_REGEX,
    'raw_comps': RAW_COMPS_REGEX,
    'os_data': OS_DATA_REGEX,
    'comps': COMPS_REGEX,
    'gdw': GDW_REGEX,
}


# Geo Index
GEO_INDEX_QA_REPORT_URL = (
    'http://lon-sql-02/ReportServer/Pages/ReportViewer.aspx?/GeographyIndexQA/GeographyIndexQA&GeoLevel='
    '{geo_level}&CurrentGeoIndexBuildRunIdAllGeos={curr_allgeos}&CurrentGeoIndexBuildRunId20CC={curr_20cc}'
    '&PreviousGeoIndexBuildRunId20CC={prev_20cc}&CurrentGeoIndexBuildRunIdPCL={curr_pcl}&PreviousGeoIndexBuildRunIdPCL='
    '{prev_pcl}&PreviousGeoIndexBuildRunIdAllGeos={prev_allgeos}&rs:Format=EXCELOPENXML'
)

GEO_INDEX_QA_REPORT_DIRECTORY = r'S:\HOMETRACK_Root\Techdev\Applications\Geography Index\{month}'
GEO_INDEX_QA_REPORT_FILE_FORMAT = 'GeographyIndexQA_{geo_level}.xlsx'
GEO_LEVELS = ['UK', 'LA', 'GOR', 'PCD', 'PCA', 'PCDPCA', 'Cities']


# NHBC
NHBC_BUCKET = 'nhbc-eu-west-2-318016054559'
NHBC_SOURCE_DIR = 'S:\\HOMETRACK_ROOT\\Techdev\\Raw Data\\020_NHBCNewBuildDataset\\data'

# Comps build reports
# BULK_TEST_REPORT_DIRECTORY = (
#     r'S:\HOMETRACK_ROOT\Hometrack\Analytics\Bulk_Tests\Comparables Build QA Reports\{month}\v{version}'
# )
BULK_TEST_REPORT_DIRECTORY = r'S:\HOMETRACK_ROOT\Hometrack\Analytics\Bulk_Tests\Comparables Build QA Reports\{month}\v{version}'


BULK_TEST_REPORTS = {
    '1_CapitalHybridBulkTest_v{version}_{primary_capital}_{secondary_capital}.pdf': (
        'http://lon-sql-02/ReportServer/Pages/ReportViewer.aspx?/CompsQA/realtimeBulkTest&'
        'bulkTestIdSecondary={secondary_capital}&bulkTestIdPrimary={primary_capital}&rs%3AParameterLanguage=en-GB&'
        'rs:Format=PDF'
    ),
    '2_RentalBulkTest_v{version}_{primary_rental}_{secondary_rental}.pdf': (
        'http://lon-sql-02/ReportServer/Pages/ReportViewer.aspx?/CompsQA/realtimeBulkTestRental&'
        'bulkTestIdSecondary={secondary_rental}&bulkTestIdPrimary={primary_rental}&rs%3AParameterLanguage=en-GB&'
        'rs:Format=PDF'
    ),
    '3a_ClientBulkTest_v{version}_{primary_client}_{secondary_client}.pdf': (
        'http://lon-sql-02/ReportServer/Pages/ReportViewer.aspx?/CompsQA/realtimeBulkTest&'
        'bulkTestIdSecondary={secondary_client}&bulkTestIdPrimary={primary_client}&rs%3AParameterLanguage=en-GB&'
        'rs:Format=PDF'
    ),
    '3b_ClientBulkTest_v{version}_{primary_client}_{secondary_client}.pdf': (
        'http://lon-sql-02/ReportServer/Pages/ReportViewer.aspx?/CompsQA/realtimeBulkTestClient&'
        'bulkTestIdSecondary={secondary_client}&bulkTestIdPrimary={primary_client}&rs%3AParameterLanguage=en-GB&'
        'rs:Format=PDF'
    ),
    '5_RentalClientBulkTest_v{version}_{primary_rental_client}_{secondary_rental_client}.pdf': (
        'http://lon-sql-02/ReportServer/Pages/ReportViewer.aspx?/CompsQA/realtimeBulkTestClientREntal&'
        'bulkTestIdSecondary={secondary_rental_client}&bulkTestIdPrimary={primary_rental_client}&'
        'rs%3AParameterLanguage=en-GB&rs:Format=PDF'
    )
}
