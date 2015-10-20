<b>Description:</b>
Simple python script that downloads publichd torrents for all the shows you are following on pogdesign.co.uk/cat.<br>

<b>Usage:</b>
From command line, run:<br>
pd2torrent.py [-h] [-d DATE] [-f FOLDER] [-u USERNAME]<br>

optional arguments:<br>
  -h, --help            show this help message and exit<br>
  -d DATE, --date DATE  Download shows that aired on that date (yyyy/mm/dd).<br>
                        Default is today<br>
  -s START DATE, --start_date Download shows that aired from that date (yyyy/mm/dd) until --end_date<br>
  -e END_DATE, --end_date Download torrents that aired from --start_date until end_date. Default is today<br>
  -f FOLDER, --folder FOLDER<br>
                        Folder where the torrents will be downloaded.<br>
  -u USERNAME, --username USERNAME<br>
                        Username to log into pogdesign. Empty by default, so<br>
                        it will download all the shows<br>

You can store your credentials direclty on pd2torrent.conf, or you<br>
can use -u argument to provide your username and password every time you launch it<br>

<b>Requirements:</b>
Python 2.7<br>
pip: requests, beautifulsoup4, guessit
