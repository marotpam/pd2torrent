import requests
from bs4 import BeautifulSoup
from show_country_parser import get_american_shows
from show_country_parser import get_british_shows
from date_helper import *


POGDESIGN_URL = "https://www.pogdesign.co.uk/cat/"


"""Gets html code from the page with the user logged in"""
def get_login_html(username, password, url_date):
    with requests.Session() as c:
        login_data = {'username': username, 'password': password, 'sub_login': ''}
        headers_data = {"Referer":"https://www.pogdesign.co.uk/cat/login"}
        r = c.post(POGDESIGN_URL+'login', data=login_data, headers=headers_data, allow_redirects=True)

        page = c.get(POGDESIGN_URL+url_date)
        return BeautifulSoup(page.text, "lxml")


def get_downloadable_episodes(today_episodes, yesterday_episodes):
    downloadable_episodes = []
    british_shows = get_british_shows()
    american_shows  = get_american_shows()

    for episode in today_episodes:
        if episode['summary'] in american_shows:
            downloadable_episodes.append(episode)

    for episode in yesterday_episodes:
        if episode['summary'] in british_shows:
            downloadable_episodes.append(episode)

    return downloadable_episodes


def get_episodes_aired_on_date( parsed_html, date ):
    episodes = {}
    today_block = parsed_html.find( id="d_"+str( date.day ) + "_" + str( date.month ) + "_" + str( date.year ) )
    episode_divs = today_block.select( 'div' )

    for episode_div in episode_divs:
        episode_link = episode_div.p.select( 'a[href]' )
        episode_info = get_episode_info_from_link(episode_link)

        if episode_info['title'] not in episodes.keys():
            episodes[episode_info['title']] = []

        episodes[episode_info['title']].append(episode_info)

    return get_merged_episodes(episodes)


def get_merged_episodes(episodes):
    merged_episodes = []

    for episode_title, episodes in episodes.items():
        episode_numbers = [episode['episode'] for episode in episodes]
        merged_episode = episodes[0]
        merged_episode['episode'] = "e".join(episode_numbers)
        merged_episodes.append(merged_episode)

    return merged_episodes


def get_episode_info_from_link( episode_link ):
    summary = 'cat/' + episode_link[0]['href']
    title = episode_link[0].string
    episode_info = episode_link[1].string
    pattern = re.compile('\d+')
    matches = pattern.findall(episode_link[1].string)
    episode_info = {'title': str(title), 'season': str(matches[0]), 'episode': str(matches[1]), 'summary': summary}
    return episode_info


def get_url_suffix_from_date(date):
    if is_date_from_current_month(date):
        return ''
    else:
        return "{0}-{1}".format(date.month, date.year )


def get_month_html(username, password, date):
    date_url = get_url_suffix_from_date(date)
    return get_login_html( username, password, date_url )


def get_episodes_aired_on_dates(username, password, dates):
    episodes_aired_info = []

    for i, current_date in enumerate( dates ):
        print ("Searching torrents for episodes aired on {}".format(current_date))
        if i == 0:
            previous_date = get_previous_day(current_date)
            monthly_calendar_html_previous = get_month_html( username, password, previous_date )
            monthly_calendar_html_current = get_month_html(username, password, current_date)
        elif are_dates_from_different_months(previous_date, current_date):
            monthly_calendar_html_previous = monthly_calendar_html_current
            monthly_calendar_html_current = get_month_html(username, password, current_date)

        today_episodes = get_episodes_aired_on_date( monthly_calendar_html_current, current_date )
        yesterday_episodes = get_episodes_aired_on_date( monthly_calendar_html_previous, previous_date)

        episodes_aired_info += get_downloadable_episodes(today_episodes, yesterday_episodes)

        previous_date = current_date
        monthly_calendar_html_previous = monthly_calendar_html_current
    return episodes_aired_info
