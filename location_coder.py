import time

from geopy.geocoders import Nominatim
import json
import os


def read_data():
    folder_path = os.getcwd()
    filename_prefix = 'data'

    json_list = []

    for filename in os.listdir(folder_path):
        if filename.startswith(filename_prefix) and filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                json_list.extend(data)

    return json_list


if __name__ == '__main__':
    geolocator = Nominatim(user_agent="airbnb_scrapper-location_coder")

    data = read_data()

    data = [listing for listing in data if listing is not None]

    for listing in data:
        location = ""
        if listing['city']:
            location = listing['city']
            if region := listing['district']:
                location += ', ' + region
            if country := listing['country']:
                location += ', ' + country

        if location == "":
            listing['latitude'] = None
            listing['longitude'] = None
            continue

        location = geolocator.geocode(location)

        if location is not None:
            listing['latitude'] = location.latitude
            listing['longitude'] = location.longitude
            print(f"{location} - {location.latitude}, {location.longitude}")

        json.dump(data, open("data_with_coordinates.json", "w"), indent=4)
        time.sleep(1)

