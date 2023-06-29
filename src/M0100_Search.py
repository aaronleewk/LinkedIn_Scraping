"""
Get list of linkedin profiles
"""
from dotenv import load_dotenv
import sys
import os
import time
import datetime
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
search_url = os.getenv("url") # Make sure url link is to first page
max_length = int(os.getenv("search_length"))
main_url = "https://www.linkedin.com/login"

#Procedure start:
driver = Utilities.init_Selenium_driver()

driver.get(main_url)
time.sleep(2)

driver.find_element(By.NAME,'session_key').send_keys(login_user)
driver.find_element(By.NAME,'session_password').send_keys(login_pass)
driver.find_element(By.XPATH,"//button[@class='btn__primary--large from__button--floating']").click()

driver.get(search_url)
time.sleep(5)

search_page = driver.page_source
time.sleep(5)

html = BeautifulSoup(search_page, "lxml")

search_results = html.find('div', {'class':'search-results-container'})

if "No results found" in search_results.text:
    sys.exit("No results found")
else:
    print('Search results found. Scrapping links.')
    list_of_urls = []
    urls = Utilities.get_urls(driver, 0, list_of_urls, max_length)

urls = list(set(urls))

date = str(datetime.date.today())

try:
    os.mkdir('Data/%s' %date)
except:
    pass

with open('Data/%s/M0100_search_results.json' %date, 'w') as file:
    file.write(json.dumps(urls, ensure_ascii=False))
    file.close()

