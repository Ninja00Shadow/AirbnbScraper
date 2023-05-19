from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

import ListingsPage
import json

import concurrent.futures


def read_links(file_name):
    with open(file_name, 'r') as file:
        return file.readlines()


def scrape_country(link):
    listing_page = ListingsPage.ListingsPage(link, driver)

    j = 0
    data_of_country = []
    while listing_page.has_next_page():
        print(f"{link.split('/')[-2]} - {j} - ", end="")
        data_of_country.extend(listing_page.get_all_data_from_listings())
        json.dump(data_of_country, open(f"data/data_partial.json", "w"), indent=4)
        listing_page.next_listing_page()
        print()
        j += 1

    json.dump(data_of_country, open(rf"data{link.split('/')[-2]}.json", "w"), indent=4)


if __name__ == '__main__':

    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--headless")

    driver = webdriver.Chrome("C:\Python\MSID\chromedriver_win32\chromedriver.exe", options=options)

    for link in read_links("links.txt"):
        scrape_country(link)

    driver.quit()
