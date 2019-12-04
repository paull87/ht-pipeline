from app.process.nhbc.manage_plot_files import download_files, upload_files
from app.process.nhbc.process_raw_plots import process_cumulative_data
import argparse
import datetime
import argparse

# Used as default if no month  is passed to the process
current_month = datetime.datetime.now().strftime('%Y%m')


def main(month):
    upload_files(month)
    process_cumulative_data(month)
    download_files(month)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-m',
        '--month',
        dest='month',
        default=current_month,
        help='Month to process in format YYYYMM',
        required=False
    )

    args = parser.parse_args()
    main(**vars(args))
