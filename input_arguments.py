import argparse
import os
import configparser
from date_helper import *

"""Returns the arguments used when the script was invoked"""


def get_parsed_arguments():
    parser = argparse.ArgumentParser(
        description='Download torrents from the shows you are following on pogdesign')
    parser.add_argument(
        '-d',
        '--date',
        help='Download shows that aired on that date (yyyy/mm/dd). Default is today',
        required=False)
    parser.add_argument(
        '-f',
        '--folder',
        help='Folder where the torrents will be downloaded. Default is torrents',
        required=False)
    parser.add_argument(
        '-u',
        '--username',
        help='Username to log into pogdesign. Empty by default, so it will download all the shows',
        required=False)
    parser.add_argument(
        '-s',
        '--start_date',
        help='Download all torrents for all days between start_date and end_date',
        required=False)
    parser.add_argument(
        '-e',
        '--end_date',
        help='End date. Today by default. Must use start_date in order to use end_date',
        required=False)
    parser.add_argument(
        '-q',
        '--quality',
        help='Video quality. Supported values are: HDTV, 720p and 1080p',
        required=False)
    parser.add_argument(
        '-t',
        '--tracker',
        help='Tracker to download the torrent from. rartv is the default',
        required=False,
        default='rartv'
    )
    return vars(parser.parse_args())


def get_tvcalendar_credentials(args, config_parser):
    if args['username']:
        username = args['username']
        password = getpass.getpass()
    else:
        username = config_parser.get('tvcalendar', 'email')
        password = config_parser.get('tvcalendar', 'password')
    return username, password


def get_video_quality(args, config_parser):
    if args['quality']:
        if not args['quality'] in ['HDTV', '720p', '1080p']:
            raise Exception(
                'Sorry, ' +
                args['quality'] +
                ' does not match any video quality supported (HDTV, 720p or 1080p)')
        quality = args['quality']
    else:
        quality = config_parser.get('tpb', 'video_quality')
    return quality


def get_today_date():
    return datetime.datetime.today().date()


def get_dates(args):
    start_date = get_date_from_arg(args['start_date'])
    if args['end_date']:
        end_date = get_date_from_arg(args['end_date'])
    else:
        end_date = get_today_date()

    return get_dates_from_range(start_date, end_date)


def get_date(args):
    if args['start_date'] or args['end_date']:
        raise Exception(
            "Sorry, you can only specify an exact date with --date or a range of dates with --start_date and --end_date")

    return get_date_from_arg(args['date'])


def get_input_arguments(forced_arguments):
    args = get_parsed_arguments()
    args.update(forced_arguments)

    config_parser = configparser.ConfigParser()
    config_parser.read(
        os.path.join(
            os.path.dirname(__file__),
            'pd2torrent.conf'))

    folder = args['folder'] if args['folder'] else config_parser.get(
        'filesystem', 'downloads_folder')
    dates = []
    date = get_date(args) if args['date'] else get_today_date()
    dates.append(date)
    if args['start_date']:
        dates = get_dates(args)
    elif args['end_date']:
        raise Exception("--start_date argument missing")

    tracker = args['tracker']
    username, password = get_tvcalendar_credentials(args, config_parser)
    quality = get_video_quality(args, config_parser)

    return username, password, folder, dates, quality, tracker
