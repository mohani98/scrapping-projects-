import requests
from bs4 import BeautifulSoup
import csv
import json
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
if __name__ == "__main__":
    naukri_lists=[]
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options)

    url="https://www.naukri.com/data-analyst-data-engineering-jobs?k=data%20analyst%2C%20data%20engineering&experience=1&cityTypeGid=9508"

    # headers = {
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    # "Accept": "application/json",
    # "Accept-Language": "en-US,en;q=0.9",
    # "Referer": "https://www.naukri.com/python-developer-jobs",
    # "appid": "105",
    # "systemid": "Naukri"
    # }
    #headers is not used with selenium but kept for reference if needed in future for requests module
    driver.get(url)
    wait = WebDriverWait(driver, 15)

    # STEP 1: Open sort dropdown
    sort_btn = wait.until(
    EC.element_to_be_clickable((By.ID, "filter-sort"))
    )
    driver.execute_script("arguments[0].click();", sort_btn)

    # STEP 2: Click Date from list
    date_option = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//a[@data-id='filter-sort-f']")
    ))
    driver.execute_script("arguments[0].click();", date_option)

    # STEP 3: Wait for jobs to refresh
    wait.until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div.cust-job-tuple")
        )
        )

    
    time.sleep(5)
    jobs=driver.find_elements(By.CSS_SELECTOR, 'div.srp-jobtuple-wrapper')
    #print(jobs)
    #print(f"Total jobs found: {len(jobs)}")
    for job in jobs:
        try:
            title=job.find_element(By.CLASS_NAME, 'title').text
            company=job.find_element(By.XPATH, '//*[@id="listContainer"]/div[2]/div/div[1]/div/div[2]/span/a[1]').text
            experience=job.find_element(By.CLASS_NAME, 'exp-wrap').text
            location=job.find_element(By.XPATH, '//*[@id="listContainer"]/div[2]/div/div[1]/div/div[3]/div/span[2]/span/span').text
            link=job.find_element(By.CLASS_NAME, 'title').get_attribute('href')
            tags=[x for x in job.find_element(By.CLASS_NAME, 'tags-gt').text.strip().split('\t')]
            day=job.find_element(By.CLASS_NAME, 'job-post-day').text
            #print(f"Title: {title},Company: {company},Experience: {experience},Location: {location},Link: {link},Tags: {tags},Posted: {day}")
            lists_of_jobs={
                "Title": title,
                "Company": company,
                "Experience": experience,
                "Location": location,
                "Link": link,
                "Tags": tags,
                "Posted": day
                }
            naukri_lists.append(lists_of_jobs)
                    
        except Exception as e:
            print("skipping one job due to error:",e)
    driver.quit()
    with open("naukri_jobs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Title", "Company", "Experience", "Location", "Link", "Tags", "Posted"])
        writer.writeheader()
        for job in naukri_lists:
            writer.writerow(job)        