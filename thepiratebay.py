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

THEPIRATEBAY_URL = "https://thepiratebay.cr/"

"""Gets the html code from the specified URL using BeautifulSoup library"""


def get_html(url):
    page = urllib.request.urlopen(url)

    if page.info().get('Content-Encoding') == 'gzip':
        buf = BytesIO(page.read())
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


def get_torrent_url(episode_info, quality='', tracker=''):
    urls = []

    query_string = urlencode(
        episode_info['title'] +
        " s" +
        episode_info['season'] +
        "e" +
        episode_info['episode'] +
        " " +
        quality +
        " " +
        tracker)
    search_url = THEPIRATEBAY_URL + "/search/" + query_string + "/0/7/0"
    html_content = get_html(search_url)
    torrent_links = html_content.select('a[href^="magnet:"]')

    if len(torrent_links) == 0:
        return ""

    return torrent_links[0]["href"]


def get_torrent_for_episode(episode_info, quality, tracker):
    print (
        'Searching torrents for ' +
        episode_info['title'] +
        " s" +
        episode_info['season'] +
        "e" +
        episode_info['episode'])

    episode_url = get_torrent_url(episode_info, quality)
    if not episode_url:
        episode_url = get_torrent_url(episode_info)
        if not episode_url:
            return ""

    return episode_url
