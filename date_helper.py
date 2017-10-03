import datetime
from datetime import date
from datetime import timedelta
import re


def get_date_from_arg(arg):
    if re.search('^(?:[0-9]{2})?[0-9]{2}-[0-1]?[0-9]-[0-3]?[0-9]$', arg):
        aux = arg.split('-')
        try:
            d = date(int(aux[0]), int(aux[1]), int(aux[2]))
            return d
        except ValueError:
            raise Exception(arg + ' is not a valid date')
    else:
        days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        if arg in days:
            today = date.today()
            offset = (today.weekday() - days.index(arg)) % 7
            return today - timedelta(days=offset)
        else:
            raise Exception(
                'Please provide a date with the format yyyy-mm-dd or a day ' + arg)


"""
This method returns the number of seconds from epoch start (1970-1-1) to @date
"""


def get_seconds_from_date(date):
    return int((date - datetime.date(1970, 1, 1)).total_seconds())


"""
This method returns an array containing all the dates between @start_date and @end_date
"""


def get_dates_from_range(start_date, end_date):
    dates = []
    days_count = (end_date - start_date).days

    for day_index in range(0, days_count + 1):
        dates.append(start_date + timedelta(days=day_index))

    return dates


def is_date_from_current_month(date):
    today = datetime.datetime.today()
    return today.year == date.year and today.month == date.month


def are_dates_from_different_months(first_date, second_date):
    return first_date.month != second_date.month


def get_previous_day(date):
    return date - timedelta(days=1)
