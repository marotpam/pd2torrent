import os
import codecs
import guessit
import urllib2
import requests
import getpass
from bs4 import BeautifulSoup
from StringIO import StringIO
import gzip
from date_helper import *

TPB_URL = "http://thepiratebay.cr"
TPB_TORRENT_URL = "http://torrents.thepiratebay.cr/"

"""Gets the html code from the specified URL using BeautifulSoup library"""
def get_html(url):
    print url
    page = urllib2.urlopen(url)
    if page.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( page.read())
        f = gzip.GzipFile(fileobj=buf)
        page = f.read()

    return BeautifulSoup(page, "lxml")

"""Encodes a string to be able to represent a URL"""
def urlencode(title):
    title = title.lower()
    removed = [' (uk)', ' (us)', ':', '&', '\'']
    for r in removed:
        title = title.replace(r, '')

    return title.strip().replace(' ', '%20')

"""Returns a dictionary with id->name pairs for the torrents matching tpb_search_url"""
def get_tpb_torrents(episode_info, quality = '', tracker = ''):
    urls = []

    query_string = urlencode( episode_info['title'] + " s" + episode_info['season'] + "e" + episode_info['episode'] + " " + quality + " " + tracker )
    tpb_search_url = TPB_URL + "/search/" + query_string + "/0/7/0"
    tpb_content = get_html(tpb_search_url)
    torrent_divs = tpb_content.find_all(href=re.compile("/torrent/"))
    number_of_links = len(torrent_divs)
    for t in torrent_divs:
        info = t['href'].split("/")
        if number_of_links == 1 or 'WEB-DL' not in info[3]:
            urls.append({str(info[2]) : str(info[3])})

    return urls

"""Gets the URL from which to download a torrent in tpb by its torrent_id and name"""
def get_tpb_torrent_url(torrent_info):
    torrent_id, torrent_title = torrent_info.items()[0]

    return TPB_TORRENT_URL + str( torrent_id )+ "/" + str( torrent_title )+ ".torrent"

def get_tpb_torrent_for_episode( episode_info, quality, tracker ):
    print 'Searching torrents for ' + episode_info['title'] + " s" + episode_info['season'] + "e" + episode_info['episode']

    episode_urls = get_tpb_torrents( episode_info, quality, tracker )
    if not episode_urls:
        episode_urls = get_tpb_torrents( episode_info, quality )
        if not episode_urls:
            episode_urls = get_tpb_torrents( episode_info )
            if not episode_urls:
                return ""

    return get_tpb_torrent_url(episode_urls[0])
