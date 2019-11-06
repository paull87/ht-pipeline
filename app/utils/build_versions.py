from app.settings.envs import LON_SQL_03
from app.core.sql import lon_sql_03_runner


def get_lon_sql_03_gdw_version():
    query = 'SELECT buildNumber FROM [GDW3].[dbo].[tab_buildManifest]'
    result = lon_sql_03_runner().read(query)
    return result.loc[0, 'buildNumber']


def get_lon_sql_03_os_data_version():
    query = 'SELECT buildNumber FROM os_data.meta.tab_buildManifest'
    result = lon_sql_03_runner().read(query)
    return result.loc[0, 'buildNumber']


def get_lon_sql_03_comps_version():
    query = 'SELECT currentVersion FROM comparables.dbo.tab_realtimeDataVersion'
    result = lon_sql_03_runner().read(query)
    return result.loc[0, 'currentVersion']


if __name__ == '__main__':
    print(get_lon_sql_03_gdw_version())
    print(get_lon_sql_03_os_data_version())
    print(get_lon_sql_03_comps_version())