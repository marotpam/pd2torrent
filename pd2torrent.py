"""
This script downloads all the tv shows you are following on "http://www.pogdesign.co.uk/cat/"
You can create an account and then run this script to download only the shows you are following
if you provide your credentials, or all the tv shows otherwise. Please be aware that if you write
your password to this file, it will be stored as plain text and everybody will be able to see it.
If you don't want more safety, you can launch the script with the --username parameter, and you
will be asked for your password using the getpass python module. Please note that if your credentials
are incorrect, all tv shows will be downloaded without any notice
"""

import os
import urllib
import requests
import subprocess
import shlex
from bs4 import BeautifulSoup
import datetime
import gzip
from input_arguments import get_input_arguments
from pogdesign import get_episodes_aired_on_dates
from extratorrent import get_tpb_torrent_for_episode
import pycurl

"""Downloads a file from a URL to the specified destination_folder"""
def download_file_from_url(url, destination_folder):
    """download_url, filename = url.split("?title=")"""
    filename = url.split("/")[-1]
    output = destination_folder+"/"+filename

    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' } 
    r = requests.get(url, headers=headers, stream=True)
    with open(output, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()



"""
This method downloads episodes followed by @username aired on @dates to @folder
"""
def download_episodes(username, password, folder, dates, quality, tracker):
    downloaded_episodes = 0
    aired_episodes = 0

    episodes = get_episodes_aired_on_dates(username, password, dates)

    for episode_info in episodes:
        torrent_url = get_tpb_torrent_for_episode(episode_info, quality, tracker)
        if torrent_url:
            downloaded_episodes += 1
            download_file_from_url(torrent_url, folder)
            print('OK :)')
        else:
            print('KO :(')
        aired_episodes += 1

    return downloaded_episodes, aired_episodes


def download_show_torrents(forced_args={}):
    (username, password, folder, dates, quality, tracker) = get_input_arguments(forced_args)
    t0 = datetime.datetime.now()
    try:
        downloaded_episodes, aired_episodes = download_episodes(username, password, folder, dates, quality, tracker)
        time_elapsed = datetime.datetime.now() - t0
        print ("{0}/{1} episodes downloaded in {2}".format(downloaded_episodes, aired_episodes, time_elapsed))
        return 1
    except requests.exceptions.ConnectionError:
        print ("Ooops, looks like you have no internet connection :(")
        return -1

if __name__ == "__main__":
    download_show_torrents()
