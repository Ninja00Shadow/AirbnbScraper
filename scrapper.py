from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

import ListingsPage
import json


def read_links(file_name):
    with open(file_name, 'r') as file:
        return file.readlines()


if __name__ == '__main__':
    link = "https://www.airbnb.pl/s/Francja/homes"

    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--headless")

    driver = webdriver.Chrome("C:\Python\MSID\chromedriver_win32\chromedriver.exe", options=options)

    data = []
    for link in read_links("links.txt"):
        listing_page = ListingsPage.ListingsPage(link, driver)

        for j in range(0, 10):
            print(f"{j} - ", end="")
            data.extend(listing_page.get_all_data_from_listings())
            json.dump(data, open(f"data/data_partial.json", "w"), indent=4)
            listing_page.next_listing_page()
            print()

        json.dump(data, open(rf"data{link.split('/')[-2]}.json", "w"), indent=4)
        data = []

    driver.quit()
