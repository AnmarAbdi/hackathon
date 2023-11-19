import googlemaps

def find_doctors(api_key, zip_code, keyword):
    gmaps = googlemaps.Client(key=api_key)

    # Geocode the zip code to get its latitude and longitude
    geocode_result = gmaps.geocode(zip_code)
    
    if not geocode_result:
        print("Invalid zip code")
        return

    location = geocode_result[0]['geometry']['location']
    lat, lng = location['lat'], location['lng']

    places_result = gmaps.places_nearby(
        location=(lat, lng),
        radius=50, 
        keyword=keyword
    )

    if not places_result.get('results'):
        print("No doctors found nearby.")
        return

    print("Doctors near {}:".format(zip_code))
    for place in places_result['results']:
        print(place['name'])


if __name__ == "__main__":
    api_key = 'AIzaSyDWo5LhzcaWrkXS1yUAVaKKqaprWT663QE'
    
    # Get user input for the target zip code
    target_zip_code = input("Enter the zip code to find doctors nearby: ")
    target_keyword = input("Enter a keyword (e.g., 'POC'): ")

    find_doctors(api_key, target_zip_code, target_keyword)
