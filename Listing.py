from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import time
from datetime import date


class Listing:
    closed_language_popup = False

    def __init__(self, link, driver):
        self.link = link
        self.driver = driver

        self.wait = WebDriverWait(self.driver, 5)
        self.minimal_stay = 0

    def show(self):
        self.driver.get(self.link)
        self.close_language_popup()

    def scroll_to_element_middle_screen(self, by_what, argument):
        self.wait.until(EC.presence_of_element_located((by_what, argument)))
        # driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});",
        #                       driver.find_element(by_what, argument))
        self.driver.execute_script("arguments[0].scrollIntoView()", self.driver.find_element(by_what, argument))
        self.driver.execute_script("window.scrollBy(0, -200)")

    # def select_minimum_number_of_dates(self):
    #     table_str = "//table[@class='_cvkwaj']"
    #     self.wait.until(EC.presence_of_element_located((By.XPATH, table_str)))
    #
    #     dates = self.driver.find_elements(By.XPATH, table_str)[1]
    #
    #     self.scroll_to_element_middle_screen(By.XPATH, "//div[@class='_uxnsba']")
    #
    #     dates_rows = dates.find_elements(By.TAG_NAME, "tr")
    #
    #     selected_dates = 0
    #     for row in dates_rows:
    #         for date_button in row.find_elements(By.TAG_NAME, "td"):
    #             if date_button.get_attribute("aria-disabled") == "false" and selected_dates < 2:
    #                 date_button.click()
    #                 selected_dates += 1
    #
    #         if selected_dates == 2:
    #             break

    # def get_clickable_dates(self):
    #     table_str = "//table[@class='_cvkwaj']"
    #     self.wait.until(EC.presence_of_element_located((By.XPATH, table_str)))
    #
    #     dates = self.driver.find_elements(By.XPATH, table_str)[1]
    #
    #     self.scroll_to_element_middle_screen(By.XPATH, "//div[@class='_uxnsba']")
    #
    #     dates_rows = dates.find_elements(By.TAG_NAME, "tr")
    #
    #     clickable_dates = []
    #     for row in dates_rows:
    #         for date_button in row.find_elements(By.TAG_NAME, "td"):
    #             if date_button.get_attribute("aria-disabled") == "false":
    #                 clickable_dates.append(date_button)
    #
    #     return clickable_dates

    # def select_minumum_dates(self, weekends=False):
    #     dates = self.get_clickable_dates()
    #
    #     end_buttons = []
    #     for date_button in dates:
    #         if len(end_buttons) < 2:
    #             button_date = self.get_date(date_button)
    #             label = date_button.get_attribute("aria-label")
    #             if len(end_buttons) == 0 and "Termin jest dostępny" not in label and "NaN, Invalid date, Invalid date NaN. W tym dniu możesz się tylko wymeldować. " not in label:
    #                 end_buttons.append(date_button)
    #             elif len(end_buttons) == 1:
    #                 if (button_date - self.get_date(end_buttons[0])).days >= self.minimal_stay:
    #                     end_buttons.append(date_button)
    #
    #         if len(end_buttons) == 2:
    #             break
    #
    #     if len(end_buttons) == 2:
    #         end_buttons[0].click()
    #         end_buttons[1].click()
    #     else:
    #         print("Not enough dates")

    # def select_dates_in_months(self, months, skip=0):
    #     for i in range(skip):
    #         self.change_to_next_date_page()
    #
    #     for i in range(months):
    #         self.select_minumum_dates()
    #         self.change_to_next_date_page()
    #         time.sleep(1)

    # def check_weekend(self, date: date):
    #     if date.weekday() == 5 or date.weekday() == 6:
    #         return True
    #     return False

    # def get_minimum_stay(self):
    #     table_str = "//table[@class='_cvkwaj']"
    #
    #     self.wait.until(EC.presence_of_element_located((By.XPATH, table_str)))
    #     self.clear_dates()
    #
    #     dates = self.driver.find_elements(By.XPATH, table_str)[1]
    #
    #     self.scroll_to_element_middle_screen(By.XPATH, "//div[@class='_uxnsba']")
    #
    #     dates_rows = dates.find_elements(By.TAG_NAME, "tr")
    #
    #     clicked = False
    #     for row in dates_rows:
    #         for date_button in row.find_elements(By.TAG_NAME, "td"):
    #             if date_button.get_attribute("aria-disabled") == "false" and not clicked:
    #                 date_button.click()
    #                 clicked = True
    #                 break
    #         if clicked:
    #             break
    #
    #     self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='_uxnsba']")))
    #     nights = self.driver.find_element(By.XPATH, "//div[@class='_uxnsba']")
    #     nights = nights.text
    #
    #     if nights == "Dodaj daty podróży, aby uzyskać dokładną cenę":
    #         return -1
    #
    #     nights = nights.replace("Minimalny pobyt: ", "")
    #     nights = nights.split(" ")[0]
    #
    #     self.clear_dates()
    #
    #     self.scroll_to_element_middle_screen(By.XPATH, "//div[@class='_uxnsba']")
    #
    #     return int(nights)
    #
    # def get_date(self, date_button):
    #     soup = BeautifulSoup(date_button.get_attribute("innerHTML"), 'html.parser')
    #     res_date = soup.find(lambda tag: tag.name == 'div' and tag.get('class')[-1].endswith('notranslate'))
    #     res_date = res_date['data-testid']
    #     res_date = res_date.replace("calendar-day-", "")
    #     res_date = res_date.split(".")
    #     res_date = date(int(res_date[2]), int(res_date[1]), int(res_date[0]))
    #     return res_date
    #
    # def clear_dates(self):
    #     self.scroll_to_element_middle_screen(By.XPATH, "//div[@class='_1sl8tba']")
    #
    #     self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='_1sl8tba']")))
    #     clear_dates_button = self.driver.find_element(By.XPATH, "//div[@class='_1sl8tba']")
    #     clear_dates_button.click()
    #
    #     time.sleep(0.5)
    #     self.driver.implicitly_wait(10)

    # def change_to_next_date_page(self):
    #     XPath = "//button[@aria-label='Przesuń do przodu, żeby przejść do kolejnego miesiąca.']"
    #     self.wait.until(EC.presence_of_element_located((By.XPATH, XPath)))
    #     next_date_page_button = self.driver.find_element(By.XPATH, XPath)
    #
    #     next_date_page_button.click()
    #
    # def change_to_previous_date_page(self):
    #     XPath = "//button[@aria-label='Przesuń do tyłu, żeby przejść do poprzedniego miesiąca.']"
    #     self.wait.until(EC.presence_of_element_located((By.XPATH, XPath)))
    #     previous_date_page_button = self.driver.find_element(By.XPATH, XPath)
    #
    #     previous_date_page_button.click()

    def close_language_popup(self):
        try:
            if self.closed_language_popup:
                return
            language_popup = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='_1piuevz']")))

            language_close_button = language_popup.find_element(By.XPATH, "//button[@aria-label='Zamknij']")
            language_close_button.click()

            self.wait.until(EC.invisibility_of_element(language_popup))
            self.closed_language_popup = True
        except TimeoutException:
            pass

    def close_privacy_popup(self):
        try:
            privacy_popup = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='_1amw1ek']")))

            privacy_close_button = privacy_popup.find_element(By.XPATH,
                                                              "//button[@class='l1j9v1wn bmx2gr4 c1ih3c6 f1hzc007 dir dir-ltr']")
            privacy_close_button.click()

            self.wait.until(EC.invisibility_of_element(privacy_popup))
        except TimeoutException:
            pass

    # def get_prices_in_months(self, months, skip=0):
    #     self.scroll_to_element_middle_screen(By.XPATH, "//div[@class='_uxnsba']")
    #
    #     for i in range(0, skip):
    #         self.change_to_next_date_page()
    #         time.sleep(1)
    #
    #     prices = []
    #     for i in range(0, months):
    #         try:
    #             self.select_minimum_number_of_dates()
    #             prices.append(self.get_price())
    #         except:
    #             prices.append(-1)
    #             self.clear_dates()
    #         self.change_to_next_date_page()
    #         time.sleep(1)
    #
    #     return prices

    def get_name(self):
        name_str = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='_b8stb0']")))
        soup = BeautifulSoup(name_str.get_attribute("outerHTML"), 'html.parser')
        name = soup.find('div', {'class': '_b8stb0'}).text
        return name

    def get_price(self):
        price_str = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='_m6lwl6']")))
        price = BeautifulSoup(price_str.get_attribute("outerHTML"), 'html.parser')
        price = price.find('div', {'class': '_m6lwl6'}).text
        price = price.split(" zł")[0]
        price = price.replace(" ", "")
        price = float(price)

        return price

    def get_number_of_reviews(self):
        reviews_str = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@class='l1j9v1wn bbkw4bl "
                                                                                "c1rxa9od dir dir-ltr']")))
        reviews_str = reviews_str.text
        if " recenzja" in reviews_str:
            reviews_str = reviews_str.replace(" recenzja", "")
        elif " recenzje" in reviews_str:
            reviews_str = reviews_str.replace(" recenzje", "")
        elif " recenzji" in reviews_str:
            reviews_str = reviews_str.replace(" recenzji", "")
        else:
            return None

        return int(reviews_str)

    def get_rating(self):
        wait = WebDriverWait(self.driver, 3)
        try:
            rating_str = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='_17p6nbba']")))
        except TimeoutException:
            return None

        rating = rating_str.text
        rating = rating.split(" ")[0]
        rating = rating.replace(",", ".")
        return float(rating)

    def get_number_of_guests(self):
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//li[@class='l7n4lsf dir dir-ltr']")))
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        guests = soup.find_all('li', {'class': 'l7n4lsf'})
        for potential_guests in guests:
            if "gości" in potential_guests.text:
                guests = potential_guests.text
                guests = guests.split(" ")[0]
                if "Ponad " in guests:
                    guests = guests.replace("Ponad ", "")
                    guests = guests.replace(" gości · ", "")
                guests = int(guests)
                return guests

        return None

    def get_location(self):
        location_str = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='_9xiloll']")))
        city, region, country = location_str.text.split(", ")
        return city, region, country

    def get_link(self):
        return self.link

    def set_link(self, link):
        self.link = link

    def get_all_data(self):
        city, region, country = self.get_location()

        data = {"name": self.get_name(),
                "number of reviews": self.get_number_of_reviews(),
                "rating": self.get_rating(),
                "number of guests": self.get_number_of_guests(),
                "city": city,
                "region": region,
                "country": country,
                "link": self.get_link(),
                "price": self.get_price()}

        return data
