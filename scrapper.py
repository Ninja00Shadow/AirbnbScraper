from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

import ListingsPage

if __name__ == '__main__':
    link = "https://www.airbnb.pl/s/Francja/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes" \
           "&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE" \
           "&query=Francja&place_id=ChIJMVd4MymgVA0R99lHx5Y__Ws&date_picker_type=calendar&source" \
           "=structured_search_input_header&search_type=user_map_move&ne_lat=62.41848525804775&ne_lng=66" \
           ".33349524023686&sw_lat=-45.232158573346844&sw_lng=-17.121399779294393&zoom=3&zoom_level=3&search_by_map" \
           "=true&monthly_start_date=2023-06-01&monthly_length=3 "

    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--blink-settings=imagesEnabled=false")
    # options.add_argument("--headless")

    driver = webdriver.Chrome("C:\Python\MSID\chromedriver_win32\chromedriver.exe", options=options)

    listing_page = ListingsPage.ListingsPage(link, driver)

    data_list = listing_page.get_all_data_from_listings()
    for data in data_list:
        print(data)

    driver.quit()
