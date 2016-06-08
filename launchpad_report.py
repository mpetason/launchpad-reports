#
#
#
from launchpadlib.launchpad import Launchpad
from datetime import timedelta, datetime
import argparse

cachedir = ".launchpadlib/cache/"
launchpad = Launchpad.login_anonymously('just testing', 'production', cachedir, version='devel')

def created_bugs(user, start_date):
    lp_user = launchpad.people(user)
    return lp_user.searchTasks(owner=lp_user,created_since=start_date,status=[
                   "New","Opinion","Invalid","Won't Fix","Expired","Confirmed","Triaged",
                   "In Progress","Fix Committed","Fix Released","Incomplete (with response)",
                   "Incomplete (without response)"
                   ])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Launchpad Bug Reports per User')
    parser.add_argument('-u', '--usernames', nargs="+", 
                        help = 'enter usernames separated by spaces.',
                        required = True)
    parser.add_argument('-d', '--days', help = 'number of days to go back.',
                        type=int)
    parser.add_argument('-a', '--after', 
                        help = 'Search for bugs created After this date. Date is in Y-M-D format')
    args = parser.parse_args()

    if not args.after:
        start_date = datetime.today() - timedelta(days=args.days)
    else: 
        start_date = args.after
    filtered_bugs = {}
    for user in args.usernames:
        filtered_bugs[user] = created_bugs(user, start_date)
        bug_count = 0
        for bug in filtered_bugs[user]:
            bug_count = bug_count + 1
            print "[" + str(bug_count) + "]" + "[" + user + "]" + "[" + bug.web_link + "]"

