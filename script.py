"""
This is an example script that can be added to your cron to launch the pd2torrent.py script periodically
Every time it is executed, it stores the date in a file called timestamp.log, stored inside the pd2torrent
parent directory. Then, the next time it is used, it sets that date as the --start_date for the pd2torrent.py
This way, it downloads all your episodes from the last time it was executed. The first time it will only 
download episodes for that day and it will create the timestamp.log file as mentioned above.
Please make sure this script and pd2torrent.py are both runnable before launching them
"""

import os.path as path
from datetime import datetime, timedelta
import pickle
from pd2torrent import download_show_torrents


def get_last_executed_date(file_path):
    if path.isfile(file_path):
        with open(file_path, 'rb') as timestamp_serialized:
            previousTime = pickle.load(timestamp_serialized)
            return previousTime + timedelta(days=1)


def main():
    logfilePath = path.join(path.dirname(__file__), 'timestamp.log')

    today = datetime.now().date()
    last_download_date = get_last_executed_date(logfilePath)
    date = today if last_download_date is None else last_download_date

    result = download_show_torrents({'start_date': str(date)})
    if result > 0:
        with open(logfilePath, 'wb') as handle:
            pickle.dump(today, handle)


if __name__ == "__main__":
    main()
