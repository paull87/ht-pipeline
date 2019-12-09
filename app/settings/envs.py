import os

# Servers
DEV_SQL_01 = 'DEV-SQL-01\SQLDEV'
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
    'lon-sql-01': LON_SQL_01,
    'dev-sql-01': DEV_SQL_01,
    'lon-sql-06': LON_SQL_06_GEOINDEXAPP,
}

ADHOC_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'adhoc_files')

DATA_ENGINEERING_CHANNEL = '#ht-data-engineers'


# Backup File Directories
LON_SQL_04_DB_BACKUPS = 'D:\MSSQL\BACKUP'
LON_SQL_06_DB_BACKUPS = 'E:\MSSQL\Backup'

LON_SQL_01_RAW_COMPS_BACKUPS = r'\\lon-sql-01\DBRepository\rawComparables\2019'
LON_SQL_01_COMPS_BACKUPS = r'\\lon-sql-01\DBRepository\comparables\2019'
LON_SQL_01_NHBC_BACKUPS = r'\\lon-sql-01\DBRepository\nhbc'
LON_SQL_01_OS_DATA_BACKUPS = r'\\lon-sql-01\DBRepository\os_data\2019'

BACKUP_DIRS = {
    'lon-sql-01': {
        'nhbc': LON_SQL_01_NHBC_BACKUPS,
        'raw_comps': LON_SQL_01_RAW_COMPS_BACKUPS,
        'comps': LON_SQL_01_COMPS_BACKUPS,
        'os_data': LON_SQL_01_OS_DATA_BACKUPS,
    },
    'dev-sql-01': {
        'nhbc': LON_SQL_01_NHBC_BACKUPS,
        'raw_comps': LON_SQL_01_RAW_COMPS_BACKUPS,
        'comps': LON_SQL_01_COMPS_BACKUPS,
        'os_data': LON_SQL_01_OS_DATA_BACKUPS,
    },
    'lon-sql-06': {
        'nhbc': LON_SQL_06_DB_BACKUPS,
        'raw_comps': LON_SQL_06_DB_BACKUPS,
        'comps': LON_SQL_06_DB_BACKUPS,
        'os_data': LON_SQL_06_DB_BACKUPS,
    }
}

RAW_COMPS_REGEX = r'^rawComparables_v?{version_number}_\d\d\d\d_\d+_\d+.bak$'
NHBC_REGEX = r'^NHBC_v?{version_number}.bak$'
OS_DATA_REGEX = r'^OS_Data_v?{version_number}.bak$'

BACKUP_REGEXS = {
    'nhbc': NHBC_REGEX,
    'raw_comps': RAW_COMPS_REGEX,
    'os_data': OS_DATA_REGEX,
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