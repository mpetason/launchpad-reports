#
#
#
from launchpadlib.launchpad import Launchpad
from datetime import timedelta, datetime
import argparse

cachedir = ".launchpadlib/cache/"
launchpad = Launchpad.login_anonymously('just testing', 'production', cachedir, version='devel')

def created_bugs(user, start_date):
    output = {}
    lp_user = launchpad.people(user)
    for bugs in lp_user.searchTasks(owner=lp_user,created_since=start_date):
        output.setdefault(user, [])
        output[user].append(bugs)
    return output

#def created_bugs(users):
#    output = {}
#    for user in users:
#        for i in launchpad.people(user).searchTasks(status=[
#                                "New","Opinion","Invalid",
#                                "Won't Fix","Expired","Confirmed","Triaged",
#                                "In Progress","Fix Committed","Fix Released",
#                                "Incomplete (with response)",
#                                "Incomplete (without response)"]):
#             if i.owner.name == user:
#                 output.setdefault(user, [])
#                 output[user].append(i)
#    return output
 
#def filter_by_days(bugs, num_days, start_date):
#    date_range = datetime.today() - timedelta(days=num_days)
#    output = []
#    for bug in bugs:
#        if bug.date_created.replace(tzinfo=None) > date_range:
#            output.append(bug)
#    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Launchpad bug Reports.')
    parser.add_argument('-u', '--usernames', nargs="+", 
                        help = 'enter usernames separated by spaces.')
    parser.add_argument('-D', '--days', help = 'number of days to go back.',
                        type=int)
    parser.add_argument('-d', '--date', help = 'date in Y-M-D format')
    args = parser.parse_args()

    if not args.usernames:
        pass
 #   else:
 #       bug_reporters = args.usernames
 #       bugs = created_bugs(bug_reporters)
 #       filtered_bugs = {}
 #       for user in bug_reporters:
 #           bug_count = 0
 #           filtered_bugs[user] = filter_by_days(bugs[user], args.days, args.date)
 #           for i in filtered_bugs[user]:
 #               bug_count = bug_count + 1
 #               print "[" + str(bug_count) + "]" + "[" + user + "]" +  "[" + i.web_link + "]"
    else:
        if not args.date:
            start_date = datetime.today() - timedelta(days=args.days)
        else: 
            start_date = args.date
        filtered_bugs = {}
        for user in args.usernames:
            filtered_bugs[user] = created_bugs(user, start_date)
            bug_count = 0
            for bug in filtered_bugs[user]:
                bug_count = bug_count + 1
                print "[" + str(bug_count) + "]" + "[" + user + "]" +  "[" + bug.web_link + "]"

