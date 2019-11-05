import requests

URL = 'http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv'

DESTINATION_FILE = 'S:\\HOMETRACK_ROOT\\Techdev\\Raw Data\\084_LandRegistry\\latest\\pp-complete.csv'


def download_csv_file():
    return requests.get(URL)


def write_csv_file():
    with open(DESTINATION_FILE, 'wb') as csv_file:
        raw_data = download_csv_file()
        print('downloading file...')
        csv_file.write(raw_data.content)
        print('New csv file created.')


if __name__ == '__main__':
    write_csv_file()
