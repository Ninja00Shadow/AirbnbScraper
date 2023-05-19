if __name__ == '__main__':
    with open('amenities.txt', 'r') as file:
        amenities = file.readlines()

        unique_amenities = set(amenities)

        with open('unique_amenities.txt', 'w') as file:
            for amenity in unique_amenities:
                file.write(amenity)
