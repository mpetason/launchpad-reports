# Created by Michael Petersen
# mpetason@gmail.com
from launchpadlib.launchpad import Launchpad
from datetime import timedelta, datetime
from tabulate import tabulate
import argparse

# Launchpad needs a cache directory. Create this before running, or it will
# end up getting created.
cachedir = ".launchpadlib/cache/"
launchpad = Launchpad.login_anonymously('just testing', 'production', cachedir,
                                        version='devel')

# Function to search for created bugs by a user using the tasks option.
def bugs_created(user, start_date):
    lp_user = launchpad.people(user)
    return lp_user.searchTasks(owner=lp_user,created_since=start_date,status=[
                   "New","Opinion","Invalid","Won't Fix","Expired","Confirmed",
                   "Triaged","In Progress","Fix Committed","Fix Released",
                   "Incomplete (with response)","Incomplete (without response)"
                   ])

# Function to find comments by users. Currently shows all commented bugs - will
# add the ability to only show comments from a specific date until now
def bugs_comments(user, start_date):
    lp_user = launchpad.people(user)
    return lp_user.searchTasks(bug_commenter=lp_user,status=[
        "New","Opinion","Invalid","Won't Fix","Expired","Confirmed","Triaged",
        "In Progress","Fix Committed","Fix Released",
        "Incomplete (with response)","Incomplete (without response)"
        ])

# If running via the CLI we will offer up options.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bugs created by specified'
                                     ' users on Launchpad.')
    parser.add_argument('-u', '--usernames', nargs="+",
                        help = 'enter usernames separated by spaces.',
                        required = True)
    parser.add_argument('-d', '--days', help = 'number of days to go back.',
                        type=int)
    parser.add_argument('-a', '--after',
                        help = 'Search for bugs created After this date. '
                        'Date is in Y-M-D format')
    parser.add_argument('-c', '--comments',
                        help = 'Search for only comments created by user',
                        type=bool)
    args = parser.parse_args()

# Find the start date so that we can find bugs created after it.
    if not args.after:
        start_date = datetime.today() - timedelta(days=args.days)
    else:
        start_date = args.after
    filtered_bugs = {}
    table_bugs = []

    # If looking for created bugs, but not commented bugs
    if not args.comments:
        for user in args.usernames:
            filtered_bugs[user] = bugs_created(user, start_date)
            bug_count = 0
            for bug in filtered_bugs[user]:
                bug_count = bug_count + 1
                table_bugs.append([bug_count, user, bug.web_link,
                    bug.date_created])

    # Else find all comments by user
    else:
        for user in args.usernames:
            filtered_bugs[user] = bugs_comments(user, start_date)
            bug_count = 0
            for bug in filtered_bugs[user]:
                bug_count = bug_count + 1
                table_bugs.append([bug_count, user, bug.web_link,
                    bug.date_created])

# Printing out the data after collecting it in an easy to read format.
    print(tabulate(table_bugs, headers=["#", "Username", "Bug URL",
                                        "Date Created"], tablefmt="psql",
                                        numalign="left"))
