from app.settings.envs import LON_SQL_03
from app.core.sql import lon_sql_03_runner, lon_sql_02_sqlcen_runner


def lon_sql_03_gdw_version():
    query = 'SELECT buildNumber FROM [GDW3].[dbo].[tab_buildManifest]'
    result = lon_sql_03_runner().read(query)
    return result.loc[0, 'buildNumber']


def lon_sql_03_os_data_version():
    query = 'SELECT buildNumber FROM os_data.meta.tab_buildManifest'
    result = lon_sql_03_runner().read(query)
    return result.loc[0, 'buildNumber']


def lon_sql_03_comps_version():
    query = 'SELECT currentVersion FROM comparables.dbo.tab_realtimeDataVersion'
    result = lon_sql_03_runner().read(query)
    return result.loc[0, 'currentVersion']


def lon_sql_03_nhbc_version():
    query = 'SELECT MAX(BuildID) as BuildID FROM nhbc.nhbc.tab_build'
    result = lon_sql_03_runner().read(query)
    return result.loc[0, 'BuildID']


def lon_sql_02_sqlcen_gdw_version():
    query = 'SELECT buildNumber FROM [GDW3].[dbo].[tab_buildManifest]'
    result = lon_sql_02_sqlcen_runner().read(query)
    return result.loc[0, 'buildNumber']


def lon_sql_02_sqlcen_os_data_version():
    query = 'SELECT buildNumber FROM os_data.meta.tab_buildManifest'
    result = lon_sql_02_sqlcen_runner().read(query)
    return result.loc[0, 'buildNumber']


def lon_sql_02_sqlcen_comps_version():
    query = 'SELECT currentVersion FROM comparables.dbo.tab_realtimeDataVersion'
    result = lon_sql_02_sqlcen_runner().read(query)
    return result.loc[0, 'currentVersion']


def lon_sql_02_sqlcen_nhbc_version():
    query = 'SELECT MAX(BuildID) as BuildID FROM nhbc.nhbc.tab_build'
    result = lon_sql_02_sqlcen_runner().read(query)
    return result.loc[0, 'BuildID']


def compare_os_data_builds():
    return lon_sql_03_os_data_version() == lon_sql_02_sqlcen_os_data_version()


def compare_comps_builds():
    return lon_sql_02_sqlcen_comps_version() == lon_sql_03_comps_version()


def compare_gdw_builds():
    return lon_sql_02_sqlcen_gdw_version() == lon_sql_03_gdw_version()


def compare_nhbc_builds():
    return lon_sql_02_sqlcen_nhbc_version() == lon_sql_03_nhbc_version()


if __name__ == '__main__':
    print(compare_os_data_builds())
    print(compare_comps_builds())
    print(compare_gdw_builds())
    print(compare_nhbc_builds())
