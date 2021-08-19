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

dictionary_of_scraper_navigation = {'login':['username', 'jpmorgan-USD'], 
                                 'password': ['password', 'Marketing123!'],
                                 'enter_button': ['merchant_login_submit_button'], 
                                 'transactions_button': ['#merchant-home > div:nth-child(2) > div:nth-child(2) > div > div.actions__links > a:nth-child(1)'],
                                 'start_date_field': ['snapshot-date-start', '6/7/2021'], 
                                 'end_date_field': ['snapshot-date-end', '6/13/2021'],
                                 'submit_date_button': ['SnapshotSubmit']}


for event_name_key, actions_list_value in dictionary_of_scraper_navigation.items():

    if event_name_key in ['login', 'password']:
        website_object = driver.find_element_by_name(actions_list_value[0])
        website_object.send_keys(actions_list_value[1])
        time.sleep(random.uniform(0.5,3))

    elif event_name_key in ['enter_button', 'start_date_field', 'end_date_field', 'submit_date_button']:
        website_object = driver.find_element_by_id(actions_list_value[0])

        if event_name_key in ['enter_button', 'submit_date_button']:
            website_object.click()

            if event_name_key == 'enter_button':
                time.sleep(random.uniform(4,7))

            else:
                time.sleep(random.uniform(2,5))

        elif event_name_key in ['start_date_field', 'end_date_field']:
            website_object.clear()
            website_object.send_keys(actions_list_value[1])
            time.sleep(random.uniform(0.5,2))
    
    else:
        website_object = driver.find_element_by_css_selector(actions_list_value[0])
        website_object.click()
        time.sleep(random.uniform(3,5)) #Let next page load

dictionary_of_dataframe_scraping = {'datetime': ['//tbody/tr/td[2]/b/small', []], 
                                    'charges_count': ['//tbody/tr/td[3]/small', []], 
                                    'charges_amount': ['//tbody/tr/td[4]/small', []], 
                                    'refunds_count': ['//tbody/tr/td[5]/small', []],
                                    'refunds_amount': ['//tbody/tr/td[6]/small', []]}


for event_name_key, actions_list_value in dictionary_of_dataframe_scraping.items():
    scraping_column = driver.find_elements_by_xpath(actions_list_value[0])

    for row in scraping_column:
        actions_list_value[1].append(row.text)

dictionary_of_jpm_table_values = {'Datetime': dictionary_of_dataframe_scraping.get('datetime')[1],
                                  'Charges Count': dictionary_of_dataframe_scraping.get('charges_count')[1],
                                  'Charges Amount': dictionary_of_dataframe_scraping.get('charges_amount')[1],
                                  'Refunds Count': dictionary_of_dataframe_scraping.get('refunds_count')[1],
                                  'Refunds Amount': dictionary_of_dataframe_scraping.get('refunds_amount')[1]}

df_jpm_refund_table = pd.DataFrame(dictionary_of_jpm_table_values)

display(df_jpm_refund_table.head())
display(' ')
display(' ')
display(df_jpm_refund_table.tail())                                 