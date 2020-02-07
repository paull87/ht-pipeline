import requests
import os
import datetime
import argparse
from requests_ntlm import HttpNtlmAuth

from app.core.slack_client import send_message
from app.settings.secrets import USER_NAME, PASSWORD
from app.settings.envs import BULK_TEST_REPORTS, BULK_TEST_REPORT_DIRECTORY
from app.core.logger import logger
from app.process.comparables.build_config import get_bulk_test_ids

# Used as default if no month  is passed to the process
current_month = datetime.datetime.now().strftime('%Y-%m')


def get_report_file(url):
    """
    Creates a requests session with the authentication and retrieves the report from
    from the given url.
    """
    session = requests.Session()
    session.auth = HttpNtlmAuth(USER_NAME, PASSWORD)
    return session.get(url)


def download_report(destination_file, report_url):
    """Downloads the report for the given params and saves it the given destaination file."""
    logger.info(f'downloading report {report_url}')
    with open(destination_file, 'wb') as report_file:
        raw_data = get_report_file(report_url)
        report_file.write(raw_data.content)


def create_reports_directory(month, version):
    """Creates the month and version folders where required."""
    report_directory = BULK_TEST_REPORT_DIRECTORY.format(month=month, version=version)
    create_directory(os.path.dirname(report_directory))
    return create_directory(report_directory)


def create_directory(directory):
    """Formats the destination directory and creates it if it doesn't exist."""
    if not os.path.isdir(directory):
        logger.info(f'creating directory {directory}')
        os.mkdir(directory)
    return directory


def download_all_reports(current_version, compare_version, month=current_month):
    """
    Loops through each geo level and downloads the report.
    For the PCDPCA report, the required extra data is appended to it.
    """
    directory = create_reports_directory(month, current_version)
    bulk_test_ids = get_bulk_test_ids(current_version, compare_version)
    for file_name_fmt, report_url_fmt in BULK_TEST_REPORTS.items():
        file_name = file_name_fmt.format(version=current_version, **bulk_test_ids)
        report_url = report_url_fmt.format(version=current_version, **bulk_test_ids)
        logger.info(f'creating report for {file_name}...')
        destination_file = os.path.join(directory, file_name)
        download_report(
            destination_file=destination_file,
            report_url=report_url
        )
    send_message(
        '#ht-compsbuild',
        f'QA reports for Comps Build v{current_version} sign-off are available here:\n{directory}'
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v',
        '--version',
        dest='current_version',
        help='Current Build ID',
        required=True,
        type=int,
    )
    parser.add_argument(
        '-c',
        '--compare',
        dest='compare_version',
        help='Build ID to compare to',
        required=True,
        type=int,
    )

    args = parser.parse_args()
    download_all_reports(**vars(args))


