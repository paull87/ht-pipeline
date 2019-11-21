import requests
import os
import pandas
import openpyxl
import datetime
from requests_ntlm import HttpNtlmAuth
from app.settings.secrets import USER_NAME, PASSWORD
from app.core.sql import lon_sql_06_geoindexapp_runner

# Used as default if no month  is passed to the process
current_month = datetime.datetime.now().strftime('%Y%m')

REPORT_URL = (
    'http://lon-sql-02/ReportServer/Pages/ReportViewer.aspx?/GeographyIndexQA/GeographyIndexQA&GeoLevel='
    '{geo_level}&CurrentGeoIndexBuildRunIdAllGeos={curr_allgeos}&CurrentGeoIndexBuildRunId20CC={curr_20cc}'
    '&PreviousGeoIndexBuildRunId20CC={prev_20cc}&CurrentGeoIndexBuildRunIdPCL={curr_pcl}&PreviousGeoIndexBuildRunIdPCL='
    '{prev_pcl}&PreviousGeoIndexBuildRunIdAllGeos={prev_allgeos}&rs:Format=EXCELOPENXML'
)

DESTINATION_DIRECTORY = r'D:\Users\plucas\Downloads\{month}'
DESTINATION_FILE = 'GeographyIndexQA_{geo_level}.xlsx'
GEO_LEVELS = ['UK', 'LA', 'GOR', 'PCD', 'PCA', 'PCDPCA', 'Cities']


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
    url = REPORT_URL.format(
        geo_level=geo_level.replace(' ', '+'),
        curr_allgeos=curr_allgeos,
        prev_allgeos=prev_allgeos,
        curr_20cc=curr_20cc,
        prev_20cc=prev_20cc,
        curr_pcl=curr_pcl,
        prev_pcl=prev_pcl,
    )
    with open(destination_file, 'wb') as report_file:
        print(f'Downloading {geo_level} report.')
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
    directory = DESTINATION_DIRECTORY.format(month=month)
    if not os.path.isdir(directory):
        os.mkdir(directory)
    return directory


def download_all_reports(month=current_month):
    """
    Loops through each geo level and downloads the report.
    For the PCDPCA report, the required extra data is appended to it.
    """
    directory = create_directory(month=month)
    for geo_level in GEO_LEVELS:
        destination_file = os.path.join(directory, DESTINATION_FILE.format(geo_level=geo_level))
        download_report(
            # TODO: Take out the hardcoded numbers.
            destination_file=destination_file,
            geo_level=geo_level,
            curr_allgeos=1283,
            prev_allgeos=1280,
            curr_20cc=1282,
            prev_20cc=1279,
            curr_pcl=1281,
            prev_pcl=1278,
        )
        if geo_level == 'PCDPCA':
            data = get_extra_report_data(1283)
            append_extra_data_to_report(destination_file, data)


if __name__ == '__main__':
    download_all_reports()


