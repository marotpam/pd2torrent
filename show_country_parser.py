"""
This script can be used to determine the origin country of all shows in pogdesign DB.
"""

import os
import codecs
import urllib
import re
import requests
import argparse
import datetime
import time
import subprocess
import shlex
import getpass
from bs4 import BeautifulSoup
from io import StringIO
import gzip
import pickle

POGDESIGN_URL = "http://www.pogdesign.co.uk/cat/"
POGDESIGN_ALL_SHOWS_URL = "http://www.pogdesign.co.uk/cat/showselect.php"

SHOWS_DICT_FILENAME = 'shows_countries.pickle'

"""Gets the html code from the specified URL using BeautifulSoup library"""
def get_html(url):
    page = urllib.request.urlopen(url)
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

    return title.replace(' ', '%20')

def get_all_shows_in_pogdesign():
    show_summaries = {}

    html = get_html(POGDESIGN_ALL_SHOWS_URL)
    show_divs = html.find_all(class_='label_check')

    for show_div in show_divs:
        show_name = show_div.strong.text
        show_summary_suffix = show_div.a['href'][1:]

        show_summaries[str(show_name)] = str(show_summary_suffix)

    return show_summaries

def get_show_country(show_summary_url_suffix):
    show_summary_url = POGDESIGN_URL + show_summary_url_suffix
    html_show_summary = get_html(show_summary_url)

    summary_data_divs = html_show_summary.find(class_='sumdata').find_all('div')

    text_summary_country = summary_data_divs[3].text
    (dummy_text, show_country) = text_summary_country.split(' : ')

    return str(show_country)

def get_shows_dict_filepath():
    script_parent_folder = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_parent_folder,SHOWS_DICT_FILENAME)

def store_shows_countries(shows_dict):
    shows_dict_filepath = get_shows_dict_filepath()
    with open(shows_dict_filepath, 'wb') as handle:
        pickle.dump(shows_dict, handle)

def get_stored_shows_countries():
    shows_dict_filepath = get_shows_dict_filepath()
    with open(shows_dict_filepath, 'rb') as shows_dict_serialized:
        shows_dict = pickle.load(shows_dict_serialized)

    return shows_dict

def get_shows_countries(shows_summaries):
    shows_countries = {}

    for show_name, show_summary_url_suffix in shows_summaries.items():
        shows_countries[show_name] = get_show_country(show_summary_url_suffix)

    return shows_countries

def find_missing_shows_countries():
    stored_shows = get_stored_shows_countries()
    all_shows_summaries = get_all_shows_in_pogdesign()
    missing_shows = [missing_show for missing_show in all_shows_summaries.keys() if missing_show not in stored_shows.keys()]

    missing_shows_summaries = {}

    for missing_show in missing_shows:
        missing_shows_summaries[missing_show] = all_shows_summaries[missing_show]

    missing_shows_countries = get_shows_countries(missing_shows_summaries)

    refreshed_shows_countries = stored_shows.copy()
    refreshed_shows_countries.update(missing_shows_countries)

    print ("{0} new shows imported".format(len(missing_shows_countries)))

    store_shows_countries(refreshed_shows_countries)

def get_shows_from(country_name):
    shows_countries = get_stored_shows_countries()

    return [show for show in shows_countries.keys() if shows_countries[show] == country_name]

def get_american_shows():
    return get_shows_from('USA')

def get_british_shows():
    return get_shows_from('United Kingdom')

if __name__ == "__main__":
    find_missing_shows_countries()
