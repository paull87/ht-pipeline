from datetime import datetime
from time import sleep
from os import makedirs, remove, listdir
from os.path import exists, join
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyodbc
import xlrd


def get_logged_in_driver(username, password, download_dir):
    
    # make sure the download dir exists
    makedirs(download_dir, exist_ok=True)

    # setup Chrome
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {"download.default_directory": download_dir})
    driver = webdriver.Chrome(chrome_options=options)

    # login to CML site
    driver.get("https://www.ukfinance.org.uk/user")

    username_input = driver.find_element_by_id("edit-name")
    username_input.send_keys(username)

    password_input = driver.find_element_by_id("edit-pass")
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)
    
    return driver


def download_file_by_description(driver, description):
    
    driver.get("https://www.ukfinance.org.uk/industry-data-tables")

    # expand the data table
    associate_button = driver.find_element_by_xpath("//button[contains(text(), 'Associate - Industry Data Tables')]")
    associate_button.click()

    # find the right node
    span_node = driver.find_element_by_xpath(f"//td[.//text()='{description}']")
    row_node = span_node.find_element_by_xpath(".//ancestor::tr")
    link_node = row_node.find_element_by_xpath(".//a")

    # extract the link and file name
    url = link_node.get_attribute("href")
    file_name = url.split("/")[-1]

    # download the file
    driver.get(url)

    return file_name


def wait_for_download(path):
    
    for i in range(0, 30):
        sleep(1)
        if exists(path):
            break
        if i == 29:
            raise Exception("timed out waiting for downloads to finish")


def download_files(download_dir):

    # set required inputs
    username = "mswain@hometrack.com"
    password = "g1yJo^s7Gn*7ox7v"
    
    # delete any existing files to avoid conflicts
    if exists(download_dir):
        for f in listdir(download_dir):
            remove(join(download_dir, f))
    
    # setup the web browser
    driver = get_logged_in_driver(username, password, download_dir)

    # kick off the downloads
    ftb_file = download_file_by_description(driver, "First-time buyers, new mortgages and affordability, UK")
    movers_file = download_file_by_description(driver, "Home movers, new mortgages and affordability, UK")
    
    # wait for the downloads to finish
    for file_name in [ftb_file, movers_file]:
        wait_for_download(join(download_dir, file_name))
    
    driver.close()
    
    return ftb_file, movers_file


def process_file(full_path):
    
    MONTH_COLUMN = 1
    DATA_COLUMN = 10
    FIRST_DATA_ROW = 10

    # open the Excel doc
    wb = xlrd.open_workbook(full_path)
    sheet = wb.sheet_by_index(0)

    # check that the headers are as expected
    header = sheet.cell(3, DATA_COLUMN).value + " " + sheet.cell(9, DATA_COLUMN).value
    if header != "LTV mean":
        raise Exception("couldn't find expected header, file format may have changed")

    # check the first date in the file
    cell = sheet.cell(FIRST_DATA_ROW, MONTH_COLUMN)
    first_month = xlrd.xldate_as_datetime(cell.value, wb.datemode)

    if first_month != datetime(2005, 4, 1):
        raise Exception("expected first month of 2005-04 but got something else")
    
    # parse the data
    data = {}
    current_row = FIRST_DATA_ROW

    while True:
        # get the cell which should contain the month
        cell = sheet.cell(current_row, MONTH_COLUMN)
        # exit loop if it's a blank cell
        if not cell.value:
            break
        # parse the date to get the month
        current_month = xlrd.xldate_as_datetime(cell.value, wb.datemode)
        # record the data
        data[current_month] = sheet.cell(current_row, DATA_COLUMN).value
        # move on to the next row
        current_row += 1

    return data


def combine_datasets(ftb_data, movers_data):
    data = {}
    keys = set()

    for k in list(ftb_data.keys()) + list(movers_data.keys()):
        keys.add(k)

    for k in keys:
        data[k] = {
            "ftb": ftb_data[k] / 100.0,
            "movers": movers_data[k] / 100.0,
        }

    return data


def import_for_gdw(data):
    """
    Updates gdw_raw.dbo.imp_macroeconomic with the last 12 months LTV values
    """
    query = """
        update dbo.imp_macroeconomic
        set MedianFTBsAdvance = ?,
            MedianMoversAdvance = ?
        where [Date] = ?
    """
    connection_string = "driver={SQL Server};server=LON-SQL-03;database=gdw_raw;trusted_connection=true"

    with pyodbc.connect(connection_string, autocommit=True) as connection:
        curs = connection.cursor()
        curs.execute("set nocount on")
        for k in sorted(data.keys())[-12:]:
            curs.execute(query, data[k]["ftb"], data[k]["movers"], k)
