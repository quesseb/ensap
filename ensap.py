
import requests
import json
import os.path
import argparse
import sys
from datetime import date



####### change variables here, like URL, action URL, user, pass
base_url = 'ensap.gouv.fr'
https_base_url = 'https://' + base_url
useragent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
authentication_url = https_base_url + '/'
# username and password for login
username = ""
password = ""

#destination folder:
download_folder = '/tmp'

# creating the date object of today's date
todays_date = date.today()
current_year = todays_date.year

# Initialize parser
parser = argparse.ArgumentParser()
# Adding optional argument
parser.add_argument("-u", '--user', default='johndoe', help = "User to search")
parser.add_argument('-y', '--year', default=current_year, help = "Year to search, default to current year, 'all' for all years")
# Read arguments from command line
args = parser.parse_args()
choosen_user = args.user
choosen_year = args.year

if choosen_user == 'johndoe':
    username = '155114412345678'
    password = 'xxxxxxxx'
if choosen_user == 'pussycat':
    username = '266114412345678'
    password = 'yyyyyyyy'
if not username:
    sys.exit("username variable is empty")
if not password:
    sys.exit("password variable is empty")

#Init session, it will manahe for us cookies
s = requests.Session()

def site_login():

    # we will use this string to confirm a successfull login:
    check_string = 'Authentification OK'
    # you need a referer for most pages! and correct headers are the key
    headers={"Content-Type":"application/x-www-form-urlencoded",
    "User-agent":useragent,
    "Accept":"application/json, text/plain, */*",
    "Host":base_url,
    "Origin":https_base_url,
    "Referer":https_base_url + '/web/accueilnonconnecte'}
    payload = {
        'identifiant':username,
        'secret':password
    }

    # First POST with supplied credentials.
    loginRequest = s.post(authentication_url, data=payload, headers=headers)
    #contents = loginRequest.text
    #print(contents)
    #index = contents.find(check_string)
    # if we find it
    if loginRequest.text.find(check_string) == -1:
        sys.exit("authentication_url : authentication failed")
    else:
        print("authentication_url : authentication successfull!")

    # Second POST with "lemonap" cookie retrieved @first post
    # this URL will list available years to download and will give a second cookie (CSRF-TOKEN)
    InitUrl = https_base_url + '/prive/initialiserhabilitation/v1'
    headers={"Content-Type":"application/json; charset=UTF-8",
    "User-agent":useragent,
    "Accept":"application/json, text/plain, */*",
    "Host":base_url,
    "Origin":https_base_url,
    "Referer":https_base_url + '/web/accueilnonconnecte'}

    initRequest = s.post(InitUrl, headers=headers)
    print("InitUrl HTTP code: {}".format(initRequest.status_code))
    year_list = json.loads(initRequest.text)['listeAnneeRemuneration']
    print("Available years: {}".format(year_list))

    if choosen_year == 'all':
        for y in year_list:
            print("### Starting to browse year {}".format(y))
            site_browse(y)
    else:
        if int(choosen_year) in year_list:
            site_browse(choosen_year)
        else:
            print("{} year not available".format(choosen_year))


def site_browse(item_year):
    directory = download_folder + '/' + choosen_user + '/' + str(item_year) + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # This URL lists all available documents to download:
    yearUrl = https_base_url + '/prive/remunerationpaie/v1?annee=' + str(item_year)
    headers={"User-agent":useragent,
    "Accept":"application/json, text/plain, */*",
    "Host":base_url,
    "Origin":https_base_url,
    "Referer":https_base_url + '/web/remunerationpaie/' + str(item_year)}
    yearRequest = s.get(yearUrl, headers=headers)
    print("List of documents HTTP code: {}".format(yearRequest.status_code))
    #print("R.TEXT: {}".format(yearRequest.text))
    #print(s.cookies)

    jsonObject = json.loads(yearRequest.text)
    for doc in jsonObject:
        site_download(doc, directory)


def site_download(item_doc, directory):
    #print(doc['documentUuid'])
    # Full local path for downloading each document:
    local_file = directory + item_doc['nomDocument']
    if not os.path.isfile(local_file):
        #print("exists")
        print("{} does not exists, downloading...".format(item_doc['nomDocument']))
        data = s.get(https_base_url + '/prive/telechargerremunerationpaie/v1?documentUuid=' + item_doc['documentUuid'])
        # Save file data to local copy
        with open(local_file, 'wb')as file:
            file.write(data.content)

site_login()
