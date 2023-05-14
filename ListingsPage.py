import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

from Listing import Listing


class ListingsPage:
    def __init__(self, link, driver):
        self.link = link
        self.driver = driver

        self.wait = WebDriverWait(self.driver, 15)

        self.show()

        self.listings = []
        self.scrap_listings()

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

    def scroll_to_element_middle_screen(self, by_what, argument):
        self.wait.until(EC.presence_of_element_located((by_what, argument)))
        self.driver.execute_script("arguments[0].scrollIntoView()", self.driver.find_element(by_what, argument))
        self.driver.execute_script("window.scrollBy(0, -200)")

    def next_listing_page(self):
        self.driver.get(self.link)
        XPath = "//a[@class='l1j9v1wn c1ytbx3a dir dir-ltr']"
        self.wait.until(EC.presence_of_element_located((By.XPATH, XPath)))
        next_listing_page_button = self.driver.find_element(By.XPATH, XPath)

        self.scroll_to_element_middle_screen(By.XPATH, XPath)

        next_listing_page_button.click()

        self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='card-container']")))
        self.scrap_listings()
        self.link = self.driver.current_url

    def scrap_listings(self):
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='card-container']")))

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
            print(f"{(i + 1)*100/len(self.listings):.0f}%", end=" | ")

        return all_data
