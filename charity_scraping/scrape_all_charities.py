import requests
import time
import json
import logging
import sys

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from utils import *

# Constants
HEADER = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "referer": "https://www.google.com/",
}

BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

# Grabbing the Cmd Line Args
iteration = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])
print(iteration, start, end)

# Configuring Logging
logging.basicConfig(filename=f"charity_quick_view{iteration}.log")

# Configuring Selenium
opts = Options()
opts.binary_location = BRAVE_PATH
driverService = Service(
    r"C:\Users\Yann\Desktop\Programming Projects\MarketplaceAnalysis\LinkedInScraper\chromedriver.exe"
)
# Initializing a Chromium Instance
browser = Chrome(options=opts, service=driverService, keep_alive=True)

df = pd.read_csv(
    r"C:\Users\Yann\Desktop\Small Programming Projects\CharitySalaries\charity_scraping\health_care_charities"
)

registration_num_list = list(df.registration_number)

if end > len(registration_num_list):
    end = len(registration_num_list)

charities_info_list = []
for registration_num in registration_num_list[start:end]:
    try:
        logging.info(f"Scraping Charity Data for {registration_num}")
        charity_info_dict = {}
        charity_info_dict["BN/Registration number"] = registration_num
        for index in range(5):
            filing_period_index = str(index)
            base_quickview = f"https://apps.cra-arc.gc.ca/ebci/hacc/srch/pub/dsplyQckVw?selectedFilingPeriodIndex={filing_period_index}&selectedCharityBn={registration_num}&isSingleResult=false"
            browser.get(base_quickview)
            # Checking for Error Code
            if str(browser.current_url).endswith("errCde=500") or str(
                browser.current_url
            ).endswith("hacwxcphndler"):
                # Break from loop, filing period index out of range
                print("Out of Range")
                break
            # Explicit Wait for presence of legendLabels for Revenue and Expenses Sections
            try:
                label = WebDriverWait(browser, 1, poll_frequency=0.1).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "legendLabel"))
                )
            except TimeoutException as e:
                logging.error(
                    f"Encountered while trying to locate legendLabel, TimeoutException Raised for registration number: {registration_num}."
                )
            # Locate Main Section
            main_element = browser.find_element(by=By.TAG_NAME, value="main")
            # If index is 0, then add the list of filing period dates, doing so only once
            if index == 0:
                section = main_element.find_element(by=By.TAG_NAME, value="section")
                charity_info_dict["Reporting Period List"] = section.find_element(
                    by=By.TAG_NAME, value="ul"
                ).text
            # Parse Information
            main = BeautifulSoup(
                main_element.get_attribute("outerHTML"), features="lxml"
            )
            charity_info_dict[filing_period_index] = {}
            print("Got Main and starting extraction")
            charity_info_dict[filing_period_index][
                "Total Compensation"
            ] = get_total_compensation_dict(main)
            print("DONE: Total Compensation")
            charity_info_dict[filing_period_index]["Salary"] = get_salary_info_dict(
                main
            )
            print("DONE: Salary Info")
            charity_info_dict[filing_period_index][
                "Ongoing Programs"
            ] = get_program_info(main)
            print("DONE: Ongoing Programs")
            (
                charity_info_dict[filing_period_index]["Revenue"],
                charity_info_dict[filing_period_index]["Expenses"],
            ) = get_revenue_expenses_dicts(main)
            print("DONE: Revenue and Expenses")
            charities_info_list.append(charity_info_dict)

    except Exception as e:
        logging.critical(
            f"Unknown Error encountered with Registration Number: {registration_num}",
            exc_info=True,
        )

with open(f"charities_info{iteration}.json", "w+") as f:
    json.dump(charities_info_list, f, indent=3)

time.sleep(5)
