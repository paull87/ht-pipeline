import requests
import os
import pandas
import openpyxl
import datetime
from requests_ntlm import HttpNtlmAuth
from app.settings.secrets import USER_NAME, PASSWORD
from app.settings.envs import GEO_LEVELS, GEO_INDEX_QA_REPORT_DIRECTORY, GEO_INDEX_QA_REPORT_FILE_FORMAT, GEO_INDEX_QA_REPORT_URL
from app.core.sql import lon_sql_06_geoindexapp_runner
from app.core.logger import logger


# Used as default if no month  is passed to the process
current_month = datetime.datetime.now().strftime('%Y-%m')

PCDPDA_EXTRA_SQL = '''
WITH cte as
(
     SELECT pvt.*
     FROM
     (
      SELECT geographyName, htproptypeId, indexSource, count(indexValue) cnt
      FROM geographyIndex_{curr_allgeos}_AllGeos.dbo.tab_geographyIndexPCDPCA as gi
      GROUP BY geographyName, htproptypeId, indexSource
     ) p
     PIVOT (sum(cnt) FOR indexSource in ([PCA],[PCD],[PCA_O])) as pvt
 )
 SELECT P.*
 , indexValueCountPCA =CTE.PCA
 , indexValueCountPCD = CTE.Pcd
 , indexValueCountPCAOverall = CTE.PCA_O
 , PurePCD = CASE WHEN cte.PCA IS NULL AND cte.PCD IS NOT NULL THEN 1 ELSE 0 END
 , PurePCA = CASE WHEN cte.PCD IS NULL AND cte.PCA IS NOT NULL THEN 1 ELSE 0 END
 , backFilledPCDWithPCA = CASE WHEN cte.PCA IS NOT NULl AND cte.PCD IS NOT NULL THEN 1 ELSE 0 END
 , filledWithPCAOverall = CASE WHEN cte.PCA_O IS NOT NULL THEN 1 ELSE 0 END
 FROM cte
 RIGHT JOIN
(
 SELECT p.PCD, htproptypeId = h.N
 FROM geographyIndex_{curr_allgeos}_AllGeos.dbo.syn_tab_pcd p
  CROSS JOIN admin.toolbox.udt_getNumberTable(0,4) h
) p on cte.geographyName = p.pcd
 AND CTE.HTPropTypeId = P.htproptypeId
order by 1,2;
'''


def get_report_file(url):
    """
    Creates a requests session with the authentication and retrieves the report from
    from the given url.
    """
    session = requests.Session()
    session.auth = HttpNtlmAuth(USER_NAME, PASSWORD)
    return session.get(url)


def download_report(destination_file, geo_level, curr_allgeos, prev_allgeos, curr_20cc, prev_20cc, curr_pcl, prev_pcl):
    """Downloads the report for the given params and saves it the given destaination file."""
    url = GEO_INDEX_QA_REPORT_URL.format(
        geo_level=geo_level.replace(' ', '+'),
        curr_allgeos=curr_allgeos,
        prev_allgeos=prev_allgeos,
        curr_20cc=curr_20cc,
        prev_20cc=prev_20cc,
        curr_pcl=curr_pcl,
        prev_pcl=prev_pcl,
    )
    logger.info(f'downloading report {url}')
    with open(destination_file, 'wb') as report_file:
        raw_data = get_report_file(url)
        report_file.write(raw_data.content)


def get_extra_report_data(curr_allgeos):
    return lon_sql_06_geoindexapp_runner().read(PCDPDA_EXTRA_SQL.format(curr_allgeos=curr_allgeos))


def format_excel_sheet_columns(sheet):
    """Formats the appended data columns to standard widths."""
    for i in 'FGHIJKLMNO':
        sheet.column_dimensions[i].width = 15


def append_extra_data_to_report(filename, data):
    """Appends the given data to the end of the counts sheets"""
    writer = pandas.ExcelWriter(filename, engine='openpyxl')
    writer.book = openpyxl.load_workbook(filename)
    writer.sheets = {ws.title: ws for ws in writer.book.worksheets}
    data.to_excel(writer, header=True, sheet_name='Counts', startcol=6, index=False)
    format_excel_sheet_columns(writer.sheets['Counts'])
    writer.save()


def create_directory(month):
    """Formats the destination directory and creates it if it doesn't exist."""
    directory = GEO_INDEX_QA_REPORT_DIRECTORY.format(month=month)
    if not os.path.isdir(directory):
        logger.info(f'creating directory {directory}')
        os.mkdir(directory)
    return directory


def download_all_reports(geo_dbs, month=current_month):
    """
    Loops through each geo level and downloads the report.
    For the PCDPCA report, the required extra data is appended to it.
    """
    directory = create_directory(month=month)
    for geo_level in GEO_LEVELS:
        logger.info(f'creating report for {geo_level}...')
        destination_file = os.path.join(directory, GEO_INDEX_QA_REPORT_FILE_FORMAT.format(geo_level=geo_level))
        download_report(
            # TODO: Take out the hardcoded numbers.
            destination_file=destination_file,
            geo_level=geo_level,
            curr_allgeos=geo_dbs['allgeos'].current,
            prev_allgeos=geo_dbs['allgeos'].previous,
            curr_20cc=geo_dbs['20cc'].current,
            prev_20cc=geo_dbs['20cc'].previous,
            curr_pcl=geo_dbs['pcl'].current,
            prev_pcl=geo_dbs['pcl'].previous,
        )
        if geo_level == 'PCDPCA':
            logger.info(f'Adding extra data for PCDPCA')
            data = get_extra_report_data(geo_dbs['allgeos'].current)
            append_extra_data_to_report(destination_file, data)


if __name__ == '__main__':
    from app.process.geo_index.db_versions import geo_index_dbs

    geo_dbs = geo_index_dbs()
    download_all_reports(geo_dbs=geo_dbs, month='2019-11')


