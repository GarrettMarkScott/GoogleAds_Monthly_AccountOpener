### Project Title
Google Ads Monthly Account Opener

### Description
This program selects random Google Ad accounts from a .csv file and opens them. The terminal will display how many business days are left in the current month and how many accounts are left that have not been checked.

The user will then be prompted to enter how many accounts they would like to open. Following that, the username and email will be requested (can be hardcoded). From there, Selenium logs into Google Ads and opens the accounts at random. While this is happening, the .csv file is updated with the date. This takes the account out of the random sampling next time the program is ran in the current month.

Once a new month occurs, all clients are put back into the stack.

When new clients are aquired the can simply be added into the .csv with their account URL. *Make sure to inclue a date!* Empty values will cause a crash.


### Required Modules
- selenium (using (http://chromedriver.chromium.org/ "ChromeDriver"))
- time
- datetime
- random
- pandas

### Files used
- GoogleAds_Monthly_AccountOpener.py
- sample.csv

### Usage Tips
1. The username and email can be hardcoded.
2. The time delay in Chrome automation may need to be adjusted depending on your internet speed.
3. Please make sure there are some kind of dates in the .csv file. The program will crash on empty values.
