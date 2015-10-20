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

KICKASS_TORRENTS_URL = "https://kat.cr"

"""Gets the html code from the specified URL using BeautifulSoup library"""
def get_html(url):
    page = urllib.request.urlopen(url)

    if page.info().get('Content-Encoding') == 'gzip':
        buf = BytesIO( page.read())
        f = gzip.GzipFile(fileobj=buf)
        page = f.read()

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
    search_url = KICKASS_TORRENTS_URL + "/usearch/" + query_string + "/?field=seeders&sorder=desc"
    html_content = get_html(search_url)
    torrent_divs = html_content.find_all(href=re.compile("/torcache.net/"))
    
    number_of_links = len(torrent_divs)
    
    for t in torrent_divs:
        urls.append("https:"+t['href'])
        """if number_of_links == 1 or 'WEB-DL' not in info[3]:
            urls.append({str(info[2]) : str(info[3])})"""

    return urls

def get_tpb_torrent_for_episode( episode_info, quality, tracker ):
    print ('Searching torrents for ' + episode_info['title'] + " s" + episode_info['season'] + "e" + episode_info['episode'])

    episode_urls = get_tpb_torrents( episode_info, quality )
    if not episode_urls:
        episode_urls = get_tpb_torrents( episode_info )
        if not episode_urls:
            return ""

    return episode_urls[0]
