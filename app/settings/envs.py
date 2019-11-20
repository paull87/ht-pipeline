import os

# Servers
LON_SQL_01 = 'LON-SQL-01'
LON_SQL_01_SOURCEBUILD = 'LON-SQL-01\SOURCEBUILD'
LON_SQL_02_SQLCEN = r'LON-SQL-02\SQLCEN'
LON_SQL_03 = 'LON-SQL-03'
LON_SQL_04 = 'LON-SQL-04'
LON_SQL_10 = 'LON-SQL-10'
LON_DWN_01 = 'LON_DWN_01'
LON_SQL_06 = 'LON-SQL-06'
LON_SQL_06_GEOINDEXAPP = r'LON-SQL-06\GeoindexApp'

ADHOC_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'adhoc_files')

DATA_ENGINEERING_CHANNEL = '#ht-data-engineers'


# File Directories
LON_SQL_04_DB_BACKUPS = 'D:\MSSQL\BACKUP'

LON_SQL_01_RAW_COMPS_BACKUPS = r'\\lon-sql-01\DBRepository\rawComparables\2019'
LON_SQL_01_COMPS_BACKUPS = r'\\lon-sql-01\DBRepository\comparables\2019'