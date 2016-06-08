# launchpad-reports

Requirements: launchpadlib, simplejson

Create a cache directory: cachedir = "./launchpadlib/cache/"

The purpose of this script is to pull bugs created by a list of users and a date range.  

usage: launchpad_report.py [-h] -u USERNAMES [USERNAMES ...] [-d DAYS]
                           [-a AFTER]

Launchpad Bug Reports per User

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAMES [USERNAMES ...], --usernames USERNAMES [USERNAMES ...]
                        enter usernames separated by spaces.
  -d DAYS, --days DAYS  number of days to go back.
  -a AFTER, --after AFTER
                        Search for bugs created After this date. Date is in
                        Y-M-D format
