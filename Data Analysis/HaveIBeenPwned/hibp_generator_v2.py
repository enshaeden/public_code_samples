#!/usr/bin/python -tt
from datetime import date
import json
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


today = date.today()
year = today.year
month = today.month


def breaches_this_month(breaches_file, year, month):
    breach_list = []
    users = []
    year = str(year)
    if month < 10:
        month = str(month)
        this_month = f"{year}-0{month}"
    else:
        month = str(month)
        this_month = f"{year}-{month}"
    with open(breaches_file) as breach:
        breaches = json.load(breach)
    for i in range(0, len(breaches["BreachSearchResults"])):
        if isinstance(breaches["BreachSearchResults"][i]["Breaches"], list):
            for n in range(0, len(breaches["BreachSearchResults"][i]["Breaches"])):
                if this_month in breaches["BreachSearchResults"][i]["Breaches"][n]["AddedDate"]:
                    if breaches["BreachSearchResults"][i]["Alias"] not in users:
                        # Collect users
                        users.append(f"{breaches['BreachSearchResults'][i]['Alias']}@lyft.com")
                    if breaches["BreachSearchResults"][i]["Breaches"][n]["Name"] not in breach_list:
                        # Collect breaches
                        breach_list.append(breaches["BreachSearchResults"][i]["Breaches"][n]["Name"])
    return breach_list, users


def create_csv(users):
    with open('hibp_cleanup.csv', 'w') as f:       # print each user to the cleanup CSV file
        print('USERNAME,', file=f)           # set first line of CSV to column header
        for user in users:
            print(f"{user},", file=f)


# def check_active(users):
#     for user in users:
#         GET https://www.googleapis.com/admin/directory/v1/users/userKey
#         for key in get_dict:
#             if key == "suspended":
#                 if suspended == True:


if __name__ == "__main__":
    breaches_file = "./hibp_pwned.json"       # keep pwned file in same folder as script or designate absolute path
    breach_list = breaches_this_month(breaches_file, year, month)   # get breaches from this month of this year
    breaches = breach_list[0]        # separate breaches from tuple as breaches
    users = breach_list[1]          # separate users from tuple as users
    create_csv(users)

# TODO enrich user list with check to see if status is archived on GWorkspace https://developers.google.com/admin-sdk/directory/v1/guides/manage-users#get_user
# TODO ask user if they want the users divided by breach
# TODO print either all users or users by breach
