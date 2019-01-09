#import dependencies
import requests
import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# import selenium and related libaries
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC

# set up the chrome driver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
dir_path = os.path.dirname(os.path.realpath("padi.ipynb"))
# download the chromedriver and store in the following path
chromedriver = dir_path + "/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriver)


def main():

    # load the page
    home_url = "https://locator.padi.com/search?lang=en&location=Worldwide"
    driver.get(home_url)

    # instentiate an empty list to store the scrape output
    results = []

    # as of 1st December, PADI locater finder had listed 6512 dive shop details; with 50 listings per page it would
    # approximately 131 pages. hence we will run the script 131 times--for each page-- using the following:
    i = 1
    while i <= 131:

        # scrape the page
        html_content = driver.page_source

        # parse the html and store the results in a beautifulsoup object
        soup = BeautifulSoup(html_content, 'lxml')

        # extract the resorts for the particluar page
        resort_list = soup.find_all('ul', id='padi-store-url-link')

        # loop through resort list and extract required information from each resort
        for resort in resort_list:
            # get name of the resort
            try:
                # consustruct if else to check if string is empty
                if resort.find(class_='listing').text.strip():
                    name = resort.find(class_='listing').text.strip()
                else:
                    name = "No_Information"
            except:
                name = "No_Information"

            # get feature category of the resort
            try:
                if resort.find(class_='featureCategory').text:
                    category = resort.find(class_='featureCategory').text
                else:
                    category = "No_Information"
            except:
                category = "No_Information"

            # get center type category of the resort
            try:
                if resort.find(class_='centerTypeCategory').text:
                    centercategory = resort.find(
                        class_='centerTypeCategory').text
                else:
                    centercategory = "No_Information"
            except:
                centercategory = "No_Information"

            # get location country of the resort
            try:
                if resort.find_all('span', class_='ng-star-inserted')[5].text:
                    location_country = resort.find_all(
                        'span', class_='ng-star-inserted')[5].text
                else:
                    location_country = "No_Information"
            except:
                location_country = "No_Information"

            # get location city of the resort
            try:
                if resort.find_all('span', class_='ng-star-inserted')[3].text:
                    location_city = resort.find_all(
                        'span', class_='ng-star-inserted')[3].text
                else:
                    location_city = "No_Information"
            except:
                location_city = "No_Information"

            # store the individual resort information on a dictionary
            resort = {
                'name': name,
                'category': category,
                'centercategory': centercategory,
                'location_country': location_country,
                'location_city': location_city}


            # append the resort details to the results list
            results.append(resort)

        # define a try except in case if we approach the end of all the pages while the loop is still valid
        try:
            driver.find_element_by_css_selector(
                'i.icon-arrow-right.ng-tns-c3-0.ng-star-inserted').click()
        except:
            pass

        time.sleep(5)

        # increment i by 1
        i += 1

    # convert the result list structure into a pandas dataframe structure
    resultsdf = pd.DataFrame(results)

    # drop the duplicate rows
    resultsdf = resultsdf.drop_duplicates()

    # export the dataframe to a csv for future use
    resultsdf.to_csv("padi.csv", index=False)


if __name__ == '__main__':
    main()
