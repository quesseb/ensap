# Ensap
Download ensap documents

# Requirements
```
apt-get install python3 python3-requests
```
As an ensap customer, you need credentials. See username and secret variables

You need to assign download_folder variable to select document destination.

# Usage
This script can be run with 2 optional parameters:
```
usage: ensap.py [-h] [-u USER] [-y YEAR]
optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User to search, default to johndoe
  -y YEAR, --year YEAR  Year to search, default to current year, 'all' for all years
```
User parameter was introduced to allow multiple users to use the script.

If you need multiple users, simply replace each credentials for johndoe and other users in the script:
```
if choosen_user == 'johndoe':
    username = '155114412345678'
    password = 'xxxxxxxx'
```
