from app.core.aws import s3
import datetime
import os
import argparse

# Used as default if no month  is passed to the process
current_month = datetime.datetime.now().strftime('%Y%m')

DESTINATION_BUCKET = 'nhbc-eu-west-2-318016054559'
SOURCE_FOLDER = 'S:\\HOMETRACK_ROOT\\Techdev\\Raw Data\\020_NHBCNewBuildDataset\\data'
FILENAME_FMT = 'raw/{month}/{filename}'


def upload_single_file(file_name, file_directory, month):
    """Uploads the given file/directory to the nhbc raw bucket for the given month."""
    full_path = os.path.join(file_directory, file_name)
    print(f'Uploading file {full_path}...')
    s3.upload_file(full_path, DESTINATION_BUCKET, FILENAME_FMT.format(month=month, filename=file_name))


def upload_files(month):
    """
    Iterates over the particular months files and uplodas them to s3.
    Where a month is not given, the current month will be used.
    """
    source_directory = os.path.join(SOURCE_FOLDER, month)
    for source_file in os.listdir(source_directory):
        upload_single_file(source_file, source_directory, month)
    print('Upload complete.')


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
    upload_files(**vars(args))
