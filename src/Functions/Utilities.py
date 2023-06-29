

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json



#Utilities
def init_Selenium_driver():

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    WINDOW_SIZE = "1920,1080"
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    
    ser = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=ser,options=chrome_options)
    
    return driver


def get_urls(driver, length, urls, max_length):

    # Cumulative list of urls tracking previous recursive function calls
    collection = urls

    time.sleep(5)

    if length >= max_length:
        print('Maximum linkedIn profiles scrapped. Search is done.')
        return collection

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    html = driver.page_source

    soup = BeautifulSoup(html, "lxml")

    search_results_container = soup.find('div', {'class': 'search-results-container'})

    search_results = search_results_container.find_all('ul',{'class': 'reusable-search__entity-result-list list-style-none'})

    results_list = search_results[0].findChildren('li', recursive=False) # Only the first item is relevant; the rest contain LinkedIn advertising links 

    for block in results_list:
        profile_link = block.find("a", href=True)
        collection.append(profile_link['href'])

    print(len(collection))
    
    time.sleep(5)

    try:
        driver.find_element(By.XPATH,"//button[@aria-label='Next']").click()
        # Shows progress
        print('Next page')
        collection = get_urls(driver, len(collection), collection, max_length)
    except:
        print('No more pages. Search is done')
        return collection
    
    return collection

