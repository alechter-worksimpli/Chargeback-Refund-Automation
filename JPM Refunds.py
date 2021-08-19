#Import libs
import urllib3 as url3
import selenium
from selenium import webdriver
import time
import random
import numpy as np
import pandas as pd
from IPython.display import display

#--- MAJOR UPGRADES TO IMPROVE RESILIENCY/RELIABILITY BELOW ---
#   (See gym class scraper for more details/code)
# 1) randomly choose amongst a browser type to mask robot
# 2) Using the set_preferences method to customize parameters i.e. privacy options

#--- KEY CONSIDERATIONS FOR CRON MIGRATION
# 1) Installing chromedriver and package dependencies
# 2) Redundancy: Sendgrid email alerts with bunch of try/except statements, cronjob alert checker
# 3) Including checks to ensure I'm pulling correct values in case they change around table or other definitions
#   i.e. take a screenshot and a make sure it looks close enough


PATH = '/Users/adrianlechter/Downloads/chromedriver_2'

#Create chromedriver object and visit JPM website
driver = webdriver.Chrome(PATH) 
time.sleep(random.uniform(2.5,5))
driver.get('https://saltpayments.transactiongateway.com/merchants/login.php')

#Input username
login = driver.find_element_by_name('username')
login.send_keys("jpmorgan-USD")
time.sleep(random.uniform(0.5,3))

# #Input password
password = driver.find_element_by_name('password')
password.send_keys("Marketing123!")
time.sleep(random.uniform(0.5,3))

#Press "enter"
enter_button_login = driver.find_element_by_id('merchant_login_submit_button')
enter_button_login.click()
time.sleep(random.uniform(4,7)) #Let login load

#Click transaction button
transactions_button = driver.find_element_by_css_selector('#merchant-home > div:nth-child(2) > div:nth-child(2) > div > div.actions__links > a:nth-child(1)')
transactions_button.click()
time.sleep(random.uniform(3,5)) #Let next page load

#Clear the start field and insert start date value
start_date_field = driver.find_element_by_id('snapshot-date-start')
start_date_field.clear()
start_date_field.send_keys('6/7/2021')
time.sleep(random.uniform(0.5,2)) #Wait to load

#Clear the end field and insert end date value
end_date_field = driver.find_element_by_id('snapshot-date-end')
end_date_field.clear()
end_date_field.send_keys('6/13/2021')
time.sleep(random.uniform(0.5,2)) #Wait to load

#Click submit button
submit_date_button = driver.find_element_by_id("SnapshotSubmit")
submit_date_button.click()
time.sleep(random.uniform(2,5)) #Wait to load


datetimes_on_table_list = []
charges_count_on_table_list = []
charges_amount_on_table_list = []
refunds_count_on_table_list = []
refunds_amount_on_table_list = []

datetimes_on_table = driver.find_elements_by_xpath('//tbody/tr/td[2]/b/small')

for datetime in datetimes_on_table:
    # print(datetime.text)
    datetimes_on_table_list.append(datetime.text)

charges_count_on_table = driver.find_elements_by_xpath('//tbody/tr/td[3]/small')

for charges_count in charges_count_on_table:
    # print(charges_count.text)
    charges_count_on_table_list.append(charges_count.text)

charges_amount_on_table = driver.find_elements_by_xpath('//tbody/tr/td[4]/small')

for charges_amount in charges_amount_on_table:
    # print(charges_amount.text)
    charges_amount_on_table_list.append(charges_amount.text)

refunds_count_on_table = driver.find_elements_by_xpath('//tbody/tr/td[5]/small')

for refunds_count in refunds_count_on_table:
    # print(refunds_count.text)
    refunds_count_on_table_list.append(refunds_count.text)

refunds_amount_on_table = driver.find_elements_by_xpath('//tbody/tr/td[6]/small')

for refunds_amount in refunds_amount_on_table:
    # print(refunds_amount.text)
    refunds_amount_on_table_list.append(refunds_amount.text)

dictionary_of_jpm_table_values = {'Datetime': datetimes_on_table_list,
                                  'Charges Count': charges_count_on_table_list,
                                  'Charges Amount': charges_amount_on_table_list,
                                  'Refunds Count': refunds_count_on_table_list,
                                  'Refunds Amount': refunds_amount_on_table_list}

# display('Datetime list has {} rows'.format(len(datetimes_on_table_list)))
# display('Charges count list has {} rows'.format(len(charges_count_on_table_list)))
# display('Charges Amount list has {} rows'.format(len(charges_amount_on_table_list)))
# display('Refunds count list has {} rows'.format(len(refunds_count_on_table_list)))
# display('Refunds amount list has {} rows'.format(len(refunds_amount_on_table_list)))

df_jpm_refund_table = pd.DataFrame(dictionary_of_jpm_table_values)

display(df_jpm_refund_table.head())
display(' ')
display(' ')
display(df_jpm_refund_table.tail())


