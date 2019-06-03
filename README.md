# 531fitness
A companion script for the 531 workout

531.py -
day, week = [0-2], [0-2] at top of file for which day/week you are in the program.
training max (tm) is set as the theoretical 1-rep-max for the given lift. 
Output is the given setxreps for each lift plus the breakdown of the weight according to given weights.
Current setup is for a 45 lb bar with weights of 45, 25, 10, 5 and 2.5.
based on the *5/3/1 For Beginners* program at r/fitness.

To be implemented:
  * code coulde use some refactoring
  * a config file could be used in place of specific values in the code
  * other workout programs could be added, such as Phraks Greyskull LP
  * could be converted to a nice little android app

# GZCLP Sheets
Modification of gzclp.py that uses Google Sheets as a database for holding weight/lift/rep configurations.
Also set up as a much cleaner OO style program.

* Requires the root directory to contain a folder called 'secret'
* In that folder should be a file called credentials.json, generated from here: https://developers.google.com/sheets/api/quickstart/python
* Folder should also contain a file called sheetId.txt, containing the sheet ID of the desired spreadsheet
  * Sheet Id can be located by url: https://docs.google.com/spreadsheets/d/[sheetId]/
  * Sheet must contain a sheet named "Parameters" with the appropriate formate
* Running script will generate token.pickle, after prompting the user to authenticate in a browser.

# Food Parser
Framework for pulling nutrition data from grocery sites.
Requires same setup as GZCLP Sheets.

Setup:

Install selenium
```
pip3 install selenium
```
Install Google Client library
```
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
Install BeautifulSoup
```
pip3 install bs4
```
Install lxml
```
pip3 install lxml
```
