from app.process.comparables.build_config import build_config, show_config
from app.process.comparables.run_build import run, latest_comps_build_version, config_compare_to_version
from app.process.comparables.generate_reports import download_all_reports
import argparse
import datetime

'''
Example usage -

Build config -

python -m app.process.comparables --action config ^
--asof 20200101 ^
--os_version 84 ^
--based_on_version 685 ^
--compared_to_version 684 ^
--rebuild False ^
--update True ^
--geo_service True


Show current config -

python -m app.process.comparables -a show


Run current config -

python -m app.process.comparables --action run ^
--description "Comps Build - Jan 2020 - Jan Release" ^
--is_release True

'''

# Used as default if no month  is passed to the process
current_month = datetime.datetime.now().strftime('%Y%m%d')


def str_to_bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def process_action(
        action,
        as_of_date,
        os_version,
        based_on_version,
        compared_to_version,
        rebuild,
        update,
        geo_service,
        build_description,
        is_release_build,
):
    if action == 'config':
        build_config(as_of_date, os_version, based_on_version, compared_to_version, rebuild, update, geo_service)
    elif action == 'show':
        show_config()
    elif action == 'run':
        run(build_description, is_release_build)
        download_all_reports(latest_comps_build_version(), config_compare_to_version())


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a',
        '--action',
        dest='action',
        help='Action to build config, show config, or run comps config',
        required=True,
        choices=['config', 'show', 'run'],
    )
    parser.add_argument(
        '-as',
        '--asof',
        dest='as_of_date',
        default=current_month,
        help='As of date for the config',
        required=False
    )

    parser.add_argument(
        '-o',
        '--os_version',
        dest='os_version',
        help='OS data version to use for the config',
        required=False
    )

    parser.add_argument(
        '-b',
        '--based_on_version',
        dest='based_on_version',
        help='Comps version based on to use for the config',
        required=False
    )

    parser.add_argument(
        '-c',
        '--compared_to_version',
        dest='compared_to_version',
        help='Comps version compared to to use for the config',
        required=False
    )

    parser.add_argument(
        '-r',
        '--rebuild',
        dest='rebuild',
        type=str_to_bool,
        help='Whether comps build is rebuild or not',
        required=False
    )

    parser.add_argument(
        '-u',
        '--update',
        dest='update',
        type=str_to_bool,
        help='Whether comps build is update or not',
        required=False
    )

    parser.add_argument(
        '-g',
        '--geo_service',
        dest='geo_service',
        type=str_to_bool,
        help='Whether comps build requires a geo service update',
        required=False
    )

    parser.add_argument(
        '-d',
        '--description',
        dest='build_description',
        help='Build description',
        required=False
    )

    parser.add_argument(
        '-i',
        '--is_release_build',
        dest='is_release_build',
        type=str_to_bool,
        help='Whether comps build is release build or not',
        required=False
    )

    args = parser.parse_args()
    process_action(**vars(args))