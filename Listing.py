from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup


class Listing:
    closed_language_popup = False

    def __init__(self, link, driver):
        self.AMENITIES_TO_LOOK_IF_IS = self.read_and_process_positive_amenities_from_file()
        self.AMENITIES_TO_LOOK_IF_NOT_FOUND = self.read_and_process_negative_amenities_from_file()
        self.link = link
        self.driver = driver

        self.wait = WebDriverWait(self.driver, 5)

    def show(self):
        self.driver.get(self.link)
        self.close_language_popup()

    def scroll_to_element_middle_screen(self, by_what, argument):
        self.wait.until(EC.presence_of_element_located((by_what, argument)))
        # driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});",
        #                       driver.find_element(by_what, argument))
        self.driver.execute_script("arguments[0].scrollIntoView()", self.driver.find_element(by_what, argument))
        self.driver.execute_script("window.scrollBy(0, -200)")

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

    def get_name(self):
        name_str = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='_b8stb0']")))
        soup = BeautifulSoup(name_str.get_attribute("outerHTML"), 'html.parser')
        name = soup.find('div', {'class': '_b8stb0'}).text
        return name

    def get_price_per_night(self):
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

    def get_general_rating(self):
        wait = WebDriverWait(self.driver, 3)
        try:
            rating_str = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='_17p6nbba']")))
        except TimeoutException:
            return None

        rating = rating_str.text
        rating = rating.split(" ")[0]
        rating = rating.replace(",", ".")
        return float(rating)

    def get_specific_ratings(self):
        wait = WebDriverWait(self.driver, 3)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='r1f90fvr dir dir-ltr']")))
        except TimeoutException:
            return [None, None, None, None, None, None]

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        ratings = soup.find_all('div', {'class': '_1s11ltsf'})
        ratings_list = []
        for rating in ratings:
            rating_value = rating.find('span', {'class': '_4oybiu'}).text
            rating_value = rating_value.replace(",", ".")
            ratings_list.append(float(rating_value))

        return ratings_list

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
        location_str = location_str.text.split(", ")
        if len(location_str) == 3:
            city, district, country = location_str
        elif len(location_str) == 2:
            city, country = location_str
            district = None
        else:
            city = None
            district = None
            country = None

        return city, district, country

    def get_link(self):
        return self.link

    def get_number_of_amenities(self):
        amenities = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='l1j9v1wn b65jmrv v7aged4 dir dir-ltr']")))
        amenities = amenities.text
        amenities = amenities.split("(")[1]
        amenities = amenities.split(")")[0]
        amenities = int(amenities)
        return amenities

    def set_link(self, link):
        self.link = link

    def get_all_data(self):
        try:
            city, region, country = self.get_location()
            cleanness, accuracy, communication, location, check_in, value = self.get_specific_ratings()
            data = {"name": self.get_name(),
                    "number of reviews": self.get_number_of_reviews(),
                    "general rating": self.get_general_rating(),
                    "number of guests": self.get_number_of_guests(),
                    "city": city,
                    "region": region,
                    "country": country,
                    "price per night": self.get_price_per_night(),
                    "number of amenities": self.get_number_of_amenities(),
                    "cleanness rating": cleanness,
                    "accuracy rating": accuracy,
                    "communication rating": communication,
                    "location rating": location,
                    "check in rating": check_in,
                    "value rating": value,
                    }

            return data
        except Exception as e:
            return None