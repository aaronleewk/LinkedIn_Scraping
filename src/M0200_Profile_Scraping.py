"""
Scrape individual linkedin profiles
"""
import sys
import os
import time
import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json
import Functions.Utilities as Utilities
from bs4 import BeautifulSoup
import Functions.Get_Profile as Get
import Functions.Generate_Insights as Insights

load_dotenv()

login_user = os.getenv("login_user")
login_pass = os.getenv("login_pass")
main_url = "https://www.linkedin.com/login"
date = str(datetime.date.today())

#Procedure start:
driver = Utilities.init_Selenium_driver()
driver.get(main_url)
time.sleep(2)

driver.find_element(By.ID,'username').send_keys(login_user)
driver.find_element(By.ID,'password').send_keys(login_pass)
driver.find_element(By.XPATH,"//button[@type='submit']").click()

time.sleep(10)

with open('Data/%s/M0100_search_results.json' % date) as file:
    urls = json.load(file)

linkedIn_profiles = []

print('Starting scraping')
for counter,each in enumerate(urls):

    try:
        
        driver.get(each)

        time.sleep(10)

        html = driver.page_source

        summary =  Get.personal_details(html)

        potential_mentor =  Insights.interested_mentoring(html)

        languages_spoken = Get.languages_list(html)

        time.sleep(2)
 
        schools = Get.education_list(html)

        time.sleep(2)

        work_exp = Get.work_exp_list(html)
        
        profile = {
            'summary':  summary,
            'potential_mentor': potential_mentor,
            'languages_spoken': languages_spoken,
            'schools': schools,
            'work_exp':  work_exp,
            'LinkedIn url': each
        }

        linkedIn_profiles.append(profile)

        time.sleep(10)
    except:
        linkedIn_profiles.append('Error scrapping this profile: ' + each)
        print('Error scrapping this profile: ' + each)
    
    print(counter)

with open('Data/%s/M0200_profile_summaries.json' % date, 'w', encoding="UTF-8") as file:
    file.write(json.dumps(linkedIn_profiles, ensure_ascii=False))

sys.exit('Finished scrapping profiles')








