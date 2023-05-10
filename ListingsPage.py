from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

import json

from Listing import Listing


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
   Call in a loop to create terminal progress bar
   @params:
       iteration   - Required  : current iteration (Int)
       total       - Required  : total iterations (Int)
       prefix      - Optional  : prefix string (Str)
       suffix      - Optional  : suffix string (Str)
       decimals    - Optional  : positive number of decimals in percent complete (Int)
       length      - Optional  : character length of bar (Int)
       fill        - Optional  : bar fill character (Str)
       printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
   """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


class ListingsPage:
    DEFAULT_CATEGORIES = ["Narciarstwo", "Przy plaży", "Przy stoku", "W pobliżu jeziora", "Biwakowanie",
                          "Z dala od cywilizacji", "W pobliżu plaży"]

    def __init__(self, link, driver, categories=DEFAULT_CATEGORIES):
        self.link = link
        self.driver = driver

        self.wait = WebDriverWait(self.driver, 10)

        self.show()

        self.listings = []
        self.scrap_listings()

        self.categories = categories
        self.category_buttons = self.get_category_buttons()

    def show(self):
        self.driver.get(self.link)
        self.close_privacy_popup()

    def close_privacy_popup(self):
        try:
            privacy_popup = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='_1amw1ek']")))

            privacy_close_button = privacy_popup.find_element(By.XPATH,
                                                              "//button[@class='l1j9v1wn bmx2gr4 c1ih3c6 f1hzc007 dir dir-ltr']")
            privacy_close_button.click()

            self.wait.until(EC.invisibility_of_element(privacy_popup))
        except TimeoutException:
            pass

    def get_category_buttons(self):
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='c8gkmzg dir dir-ltr']")))
        return iter(self.driver.find_elements(By.XPATH, "//div[@class='c8gkmzg dir dir-ltr']"))

    def next_category(self):
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='c8gkmzg dir dir-ltr']")))

        while True:
            try:
                category_button = next(self.category_buttons)
                if category_button.text in self.categories:
                    category_button.click()
                    break
                # time.sleep(1)
            except StopIteration:
                break

    def scroll_to_element_middle_screen(self, by_what, argument):
        self.wait.until(EC.presence_of_element_located((by_what, argument)))
        # driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});",
        #                       driver.find_element(by_what, argument))
        self.driver.execute_script("arguments[0].scrollIntoView()", self.driver.find_element(by_what, argument))
        self.driver.execute_script("window.scrollBy(0, -200)")

    def next_listing_page(self):
        XPath = "//a[@class='l1j9v1wn c1ytbx3a dir dir-ltr']"
        self.wait.until(EC.presence_of_element_located((By.XPATH, XPath)))
        next_listing_page_button = self.driver.find_element(By.XPATH, XPath)

        self.scroll_to_element_middle_screen(By.XPATH, XPath)

        next_listing_page_button.click()

        self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='card-container']")))
        self.scrap_listings()

    def scrap_listings(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        if self.listings:
            self.listings = []

        links = soup.find_all('div', {'data-testid': 'card-container'})

        for listing in links:
            self.listings.append(Listing("https://www.airbnb.pl/" + listing.find('a')['href'], self.driver))

    def __getitem__(self, index):
        return self.listings[index]

    def get_all_data_from_listings(self):
        all_data = []
        for i, listing in enumerate(self.listings):
            listing.show()
            all_data.append(listing.get_all_data())
            json.dump(all_data, open("data.json", "w"), indent=4)
            printProgressBar(i + 1, len(self.listings), prefix='Progress:', suffix='Complete', length=50)

        return all_data
