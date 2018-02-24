"""
This script downloads all the tv shows you are following on "http://www.pogdesign.co.uk/cat/"
You can create an account and then run this script to download only the shows you are following
if you provide your credentials, or all the tv shows otherwise. Please be aware that if you write
your password to this file, it will be stored as plain text and everybody will be able to see it.
If you don't want more safety, you can launch the script with the --username parameter, and you
will be asked for your password using the getpass python module. Please note that if your
credentials are incorrect, all tv shows will be downloaded without any notice
"""

import datetime
import os
import threading
import requests
from input_arguments import get_input_arguments
from pogdesign import get_episodes_aired_on_dates
from thepiratebay import get_torrent_for_episode

def open_magnet_link(link):
    os.system("/usr/bin/open " + link)


def download_episodes(username, password, dates, quality, tracker):
    downloaded_episodes = 0
    aired_episodes = 0

    episodes = get_episodes_aired_on_dates(username, password, dates)

    for episode_info in episodes:
        torrent_url = get_torrent_for_episode(episode_info, quality, tracker)
        if torrent_url:
            thread = threading.Thread(
                target=open_magnet_link, args=(
                    torrent_url,))
            thread.start()

            downloaded_episodes += 1
            print('OK :)')
        else:
            print('KO :(')
        aired_episodes += 1

    return downloaded_episodes, aired_episodes


def download_show_torrents(forced_args={}):
    (username, password, _, dates, quality,
     tracker) = get_input_arguments(forced_args)
    initial_time = datetime.datetime.now()
    try:
        downloaded_episodes, aired_episodes = download_episodes(
            username, password, dates, quality, tracker)
        elapsed_time = datetime.datetime.now() - initial_time
        print ("{0}/{1} episodes downloaded in {2}".format(downloaded_episodes,
                                                           aired_episodes, elapsed_time))
        return 1
    except requests.exceptions.ConnectionError as error:
        print (error)
        print ("Ooops, looks like you have no internet connection :(")
        return -1


if __name__ == "__main__":
    download_show_torrents()
