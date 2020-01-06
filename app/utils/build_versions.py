from app.settings.envs import LON_SQL_03
from app.core.sql import get_sql_runner


def gdw_version(server):
    query = 'SELECT buildNumber FROM [GDW3].[dbo].[tab_buildManifest]'
    sql_runner = get_sql_runner(server)
    result = sql_runner.read(query)
    return result.loc[0, 'buildNumber']


def os_data_version(server):
    query = 'SELECT buildNumber FROM os_data.meta.tab_buildManifest'
    sql_runner = get_sql_runner(server)
    result = sql_runner.read(query)
    return result.loc[0, 'buildNumber']


def comps_version(server):
    query = 'SELECT currentVersion FROM comparables.dbo.tab_realtimeDataVersion'
    sql_runner = get_sql_runner(server)
    result = sql_runner.read(query)
    return result.loc[0, 'currentVersion']


def raw_comps_version(server):
    query = 'SELECT currentVersion FROM rawComparables.dbo.tab_realtimeDataVersion'
    sql_runner = get_sql_runner(server)
    result = sql_runner.read(query)
    return result.loc[0, 'currentVersion']


def nhbc_version(server):
    query = 'SELECT MAX(BuildID) as BuildID FROM nhbc.nhbc.tab_build'
    sql_runner = get_sql_runner(server)
    result = sql_runner.read(query)
    return result.loc[0, 'BuildID']


if __name__ == '__main__':
    print(comps_version('lon-sql-02'), comps_version('lon-sql-03'))
    print(nhbc_version('lon-sql-02'), nhbc_version('lon-sql-03'))
    print(os_data_version('lon-sql-02'), os_data_version('lon-sql-03'))
    print(gdw_version('lon-sql-02'), gdw_version('lon-sql-03'))
    print(raw_comps_version('lon-sql-02'))


