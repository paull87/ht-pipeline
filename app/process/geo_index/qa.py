from app.core.sql import get_sql_runner
from app.process.geo_index.db_versions import geo_index_dbs
from app.core.logger import logger

LON_SQL_06_SQL_RUNNER = get_sql_runner('lon-sql-06')

COMPS_TYPES = ['Sales', 'Surveys']

geo_dbs = geo_index_dbs()

sql_query_template = '''
if OBJECT_ID('[geographyIndex_{destination_allgeos}_AllGeos].[qa].[tab_matchPair{comps_type}CS_{curr_allgeos}_{prev_allgeos}]') IS NOT NULL
    DROP TABLE [geographyIndex_{destination_allgeos}_AllGeos].[qa].[tab_matchPair{comps_type}CS_{curr_allgeos}_{prev_allgeos}]

SELECT new.*
INTO [geographyIndex_{destination_allgeos}_AllGeos].[qa].[tab_matchPair{comps_type}CS_{curr_allgeos}_{prev_allgeos}]
  FROM [geographyIndex_{curr_allgeos}_AllGeos].[qa].[tab_matchPair{comps_type}] as new
  inner join [geographyIndex_{prev_allgeos}_AllGeos].[qa].[tab_matchPair{comps_type}] as old 
					 on new.rawID1 = old.rawID1		
					 and new.rawID2 = old.rawID2
WHERE new.phase2 < {phase_id};
'''


def create_math_pair_samples(destination_allgeos, comps_type, phase_id):
    sql_query = sql_query_template.format(
        destination_allgeos=destination_allgeos,
        curr_allgeos=geo_dbs['allgeos'].current,
        prev_allgeos=geo_dbs['allgeos'].previous,
        comps_type=comps_type,
        phase_id=phase_id,
    )
    logger.info(f'Creating sample in {destination_allgeos} for {comps_type}')
    # TODO: Add sql runner call
    logger.info(sql_query)
    LON_SQL_06_SQL_RUNNER.execute(sql_query)


def create_all_samples(phase_id):
    for comps_type in COMPS_TYPES:
        create_math_pair_samples(
            destination_allgeos=geo_dbs['allgeos'].current,
            comps_type=comps_type,
            phase_id=phase_id,
        )
        create_math_pair_samples(
            destination_allgeos=geo_dbs['allgeos'].previous,
            comps_type=comps_type,
            phase_id=phase_id,
        )


if __name__ == '__main__':
    create_all_samples(234)
