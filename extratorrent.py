import os
import codecs
import urllib
import requests
import getpass
import sys
from bs4 import BeautifulSoup
from io import BytesIO
import gzip
from date_helper import *
import re

EXTRATORRENT_URL = "http://extratorrent.cc/"

"""Gets the html code from the specified URL using BeautifulSoup library"""
def get_html(url):
    page = requests.get(url).content

    return BeautifulSoup(page, "lxml")

"""Encodes a string to be able to represent a URL"""
def urlencode(title):
    title = title.lower()
    removed = [' (uk)', ' (us)', ':', '&', '\'', '!']
    for r in removed:
        title = title.replace(r, '')

    return title.strip().replace(' ', '%20')

"""Returns a dictionary with id->name pairs for the torrents matching tpb_search_url"""
def get_tpb_torrents(episode_info, quality = '', tracker = ''):
    urls = []

    query_string = urlencode( episode_info['title'] + " s" + episode_info['season'] + "e" + episode_info['episode'] + " " + quality + " " + tracker )
    search_url = EXTRATORRENT_URL + "advanced_search/?with=" + query_string + "&new=1&x=0&y=0"
    html_content = get_html(search_url)
    torrent_rows = html_content.find_all("tr", class_=re.compile('tlr|tlz'))
    
    number_of_links = len(torrent_rows)
    max_seeders = 0
    url = None
    
    for t in torrent_rows:
        seeders_column = t.find("td", class_="sy")
        if not seeders_column is None:
            seeders = int(seeders_column.text)
            if seeders > max_seeders:
                url = t.find("td", class_="tli").a["href"]
                max_seeders = seeders
        """if number_of_links == 1 or 'WEB-DL' not in info[3]:
            urls.append({str(info[2]) : str(info[3])})"""
    if not url is None:
        urls.append(EXTRATORRENT_URL + url.replace("/torrent/", "download/").replace(".html", ".torrent"))
    return urls

def get_tpb_torrent_for_episode( episode_info, quality, tracker ):
    print ('Searching torrents for ' + episode_info['title'] + " s" + episode_info['season'] + "e" + episode_info['episode'])

    episode_urls = get_tpb_torrents( episode_info, quality )
    if not episode_urls:
        episode_urls = get_tpb_torrents( episode_info )
        if not episode_urls:
            return ""

    return episode_urls[0]
