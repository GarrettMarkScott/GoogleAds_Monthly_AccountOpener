from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
import random
import pandas as pd

#Place your csv doc in this variable
client_list = 'DW_Client_List_urls.csv'


########## Calculating Number of Total Business Days in Month ##################
now = datetime.datetime.now()
date_stamp = now.strftime('%b %d')

businessdays = 0
for i in range(1, 32):
    try:
        thisdate = datetime.date(now.year, now.month, i)
    except(ValueError):
        break
    if thisdate.weekday() < 5: # Monday == 0, Sunday == 6
        businessdays += 1


######### Calculating Number of Business Days Left in the Current Month ########
businessdays_left = 0
for i in range(int(now.strftime('%d')), 32):
    try:
        thisdate = datetime.date(now.year, now.month, i)
    except(ValueError):
        break
    if thisdate.weekday() < 5: # Monday == 0, Sunday == 6
        businessdays_left += 1


############### Load CSV File into Pandas for Modification  ####################
df = pd.read_csv(client_list).set_index('Account Name')
#Adjusts dataFrame to only include clients that have not been checked
df = df.loc[df['Date Last Checked'].str.contains(str(now.strftime('%b'))) == False]

number_of_clients = len(df.index)
list_of_clients = df.index.tolist()


########################## Command Prompt ######################################
print('Hello G Dawg, there are ',businessdays_left,'business day/s left this month.' )
if number_of_clients > 1:
    print('You have ',number_of_clients,' accounts to check.')
else:
    print('You have ',number_of_clients,' account to check.')
pull_request = int(input('How many accounts would you like to open?\n'))

#These variables can be hardcoded
print('Before going any further we will need your credentials:')
userEmail = input('User Email: ')
userPassword = input('User Password: ')


########################### Select Random Accounts #############################
def chooseRandomAccount():
    randomAccount = random.sample(list_of_clients, )
    return randomAccount
randomly_selected_accounts = random.sample(list_of_clients, k=pull_request)
if pull_request > 1:
    print('Your randomly selected accounts are: \n',randomly_selected_accounts)
else:
    print('Your randomly selected account is: \n',randomly_selected_accounts)


####################### Print Date on Selected Accounts ########################
for i in randomly_selected_accounts:
    df.loc[df.index == i, 'Date Last Checked'] = date_stamp


##################### Merge & Update Original CSV File #########################
df_updated_accounts = df.loc[randomly_selected_accounts]
df_original_csv = pd.read_csv(client_list).set_index('Account Name')
df_original_csv.drop(randomly_selected_accounts, inplace=True)
df_concat = pd.concat([df_updated_accounts,df_original_csv])
df_concat.to_csv(client_list)


########################## Chrome Automation ###################################
browser = webdriver.Chrome('/Users/garrettscott/chromedriver')

browser.get('https://ads.google.com/home/')
time.sleep(2)

temp_elem = browser.find_element_by_xpath('//*[@id="jump-content"]/div[2]/section[1]/div/div/div[1]/div/a[1]').click()

user_email = browser.find_element_by_id('identifierId')
user_email.send_keys(userEmail)

email_next_button = browser.find_element_by_id('identifierNext')
email_next_button.click()
time.sleep(2)

password = browser.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
print(password.text)
#variable did not work in send_keys
password.send_keys(userPassword)
time.sleep(2)

password_next_button = browser.find_element_by_id('passwordNext')
password_next_button.click()
time.sleep(4)

account_list = browser.find_element_by_xpath('/html/body/div/root/div/nav-view-loader/multiaccount-view/div/div/material-list/material-list-item[1]/div/div[1]')
account_list.click()
time.sleep(3)

#Opens first account
browser.get(df_updated_accounts.iloc[0,2])

#Opens the following accounts
for account in randomly_selected_accounts[1:]:
    open_account = df_updated_accounts.loc[account,"Account URL"]
    browser.execute_script('''window.open('',"_blank");''')
    browser.switch_to.window(browser.window_handles[-1])
    browser.get(open_account)
