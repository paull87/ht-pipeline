from app.core.aws import s3
import datetime
import os
import argparse

# Used as default if no month  is passed to the process
current_month = datetime.datetime.now().strftime('%Y%m')

DESTINATION_BUCKET = 'nhbc-eu-west-2-318016054559'
SOURCE_FOLDER = 'S:\\HOMETRACK_ROOT\\Techdev\\Raw Data\\020_NHBCNewBuildDataset\\data'
FILENAME_FMT = 'raw/{month}/{filename}'

TRANSFORMED_FILE_PREFIX = 'transformed/plots/month={month}/part-00000-'
TRANSFORMED_FILE_NAME = 'Plots.csv'


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


def find_transformed_file(month):
    month_format = f'{month[:4]}-{month[-2:]}'
    found_files = s3.list_objects_v2(
        Bucket=DESTINATION_BUCKET, Prefix=TRANSFORMED_FILE_PREFIX.format(month=month_format)
    )['Contents']
    if len(found_files) == 1:
        return found_files[0]['Key']


def download_files(month):
    """Iterates over the transformed files and downloads the plot """
    transformed_key = find_transformed_file(month)
    if not transformed_key:
        print('No transformed file found...')
        return
    with open(os.path.join(SOURCE_FOLDER, month, TRANSFORMED_FILE_NAME), 'wb') as data:
        s3.download_fileobj(DESTINATION_BUCKET, transformed_key, data)


def process_action(state):
    actions = {
        'upload': upload_files,
        'download': download_files,
    }
    return actions[state.lower()]


def action_file(action, month):
    process = process_action(action)
    process(month)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a',
        '--action',
        dest='action',
        help='Action to upload or download plot files',
        required=True,
        choices=['upload', 'download'],
    )
    parser.add_argument(
        '-m',
        '--month',
        dest='month',
        default=current_month,
        help='Month to process in format YYYYMM',
        required=False
    )

    args = parser.parse_args()
    action_file(**vars(args))
