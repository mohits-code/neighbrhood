import requests

# Function to geocode an address to latitude and longitude using Nominatim API
def geocode_address(address):
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': address,
        'format': 'json',
        'addressdetails': 1,
        'limit': 1
    }
    headers = {
        'User-Agent': 'YourAppNameHere (your-email@example.com)'  # Replace with your actual app name and email
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:
            latitude = float(data[0]['lat'])
            longitude = float(data[0]['lon'])
            return latitude, longitude
        else:
            print("Geocoding response is empty. Please check the address.")
    else:
        print(f"Geocoding API error: {response.status_code}")
    return None, None