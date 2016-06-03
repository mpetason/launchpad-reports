#
#
#
from launchpadlib.launchpad import Launchpad
from datetime import timedelta, datetime
import argparse

cachedir = "/home/mpetason/.launchpadlib/cache/"
launchpad = Launchpad.login_anonymously('just testing', 'production', cachedir, version='devel')

def created_bugs(users):
    output = {}
    for user in users:
        for i in launchpad.people(user).searchTasks():
             if i.owner.name == user:
                 output.setdefault(user, [])
                 output[user].append(i)
    return output
 
def filter_bugs(bugs, num_days):
    date_range = datetime.today() - timedelta(days=num_days)
    output = []
    for bug in bugs:
        if bug.date_created.replace(tzinfo=None) > date_range:
            output.append(bug)
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Launchpad bug Reports.')
    parser.add_argument('-u', '--usernames', nargs="+", 
                        help = 'enter usernames separated by spaces.')
    parser.add_argument('-d', '--days', help = 'number of days to go back.',
                        type=int)
    args = parser.parse_args()

    if not args.usernames:
        pass
    else:
        bug_reporters = args.usernames
        bugs = created_bugs(bug_reporters)
        filtered_bugs = {}
        for user in bug_reporters:
            filtered_bugs[user] = filter_bugs(bugs[user], args.days)
            for i in filtered_bugs[user]:
                print "[" + user + "]" + i.web_link
