from queries import find_businesses_within_distance
from geocode import geocode_address

def main():
    print("Welcome to the neighborhood!")
    
    while True:
        # Get user input for address and distance
        address = input("Enter the address: ")
        try:
            distance = float(input("Enter distance in meters: "))
            
            # Geocode the address to get latitude and longitude
            latitude, longitude = geocode_address(address)
            if latitude is None or longitude is None:
                print("Could not geocode the address. Please try again.")
                continue

            # Call the function to find businesses within the specified distance
            businesses = find_businesses_within_distance(latitude, longitude, distance)

            # Display the results neatly
            if businesses:
                print("\nBusinesses within {:.2f} meters of '{}':".format(distance, address))
                for business in businesses:
                    print(f"- {business[0]}")
            else:
                print("\nNo businesses found within the specified distance.")

        except ValueError:
            print("Invalid input. Please enter numerical values for distance.")
        
        # Ask if the user wants to perform another search
        again = input("\nDo you want to search for another address? (yes/no): ").strip().lower()
        if again != 'yes':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
