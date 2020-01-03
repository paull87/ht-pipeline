from app.core.sql import get_sql_runner
from collections import namedtuple

GeoDB = namedtuple('GeoDB', 'current previous')

DB_TYPES = ['pcl', '20cc', 'allgeos']
LON_SQL_06_SQL_RUNNER = get_sql_runner('lon-sql-06')


def get_database_names(db_type):
    query = f'''
        SELECT LOWER([name]) as [name]
        FROM sys.databases
        WHERE LOWER([name]) LIKE 'geographyindex[_]%[_]{db_type}'
        ORDER BY [name];
    '''
    return LON_SQL_06_SQL_RUNNER.read(query)['name'].values


def geo_index_dbs():
    geo_databases = {}
    for db_type in DB_TYPES:
        databases = get_database_names(db_type)
        check_databases(databases, db_type)
        geo_databases[db_type] = database_versions(databases)
    return geo_databases


def get_database_version(database):
    try:
        version_number = database.split('_')[1]
        return int(version_number)
    except Exception as e:
        raise ValueError(
            f'Database {database} should be in format '
            f'"geographyIndex_[version]_[index_type]"'
        )


def check_databases(databases, db_type):
    assert len(databases) == 2, \
        f'There are not two databases for {db_type}'


def database_versions(databases):
    previous = get_database_version(databases[0])
    current = get_database_version(databases[1])
    return GeoDB(current=current, previous=previous)


if __name__ == '__main__':
    print(geo_index_dbs())
