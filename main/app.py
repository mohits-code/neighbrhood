import streamlit as st
from queries import find_businesses_within_distance
from geocode import geocode_address
import folium
from streamlit_folium import st_folium

def main():
    st.title("welcome to neighbrhood")

    # Input for address
    address = st.text_input("enter your location:").lower()
    
    # Input for distance
    distance = st.number_input("enter searching distance:", min_value=0, value=100, step=1)

    # Create a session state variable to store results
    if 'businesses' not in st.session_state:
        st.session_state['businesses'] = None
        st.session_state['latitude'] = None
        st.session_state['longitude'] = None

    # When the user clicks the button, geocode the address and find businesses
    if st.button("search"):
        if address:
            latitude, longitude = geocode_address(address)
            if latitude is None or longitude is None:
                st.error("could not geocode the address. please try again.")
            else:
                businesses = find_businesses_within_distance(latitude, longitude, distance)
                st.session_state['businesses'] = businesses
                st.session_state['latitude'] = latitude
                st.session_state['longitude'] = longitude

    # Display results and map if businesses are found
    if st.session_state['businesses'] is not None:
        businesses = st.session_state['businesses']
        latitude = st.session_state['latitude']
        longitude = st.session_state['longitude']
        
        if businesses:
            st.success(f"businesses within {distance:.2f} meters of '{address}':")
            business_data = []
            for business in businesses:
                st.write(f"- {business[0].lower()}")
                business_data.append({'name': business[0], 'latitude': business[1], 'longitude': business[2]})

            # Create a map centered around the searched address
            map_center = [latitude, longitude]
            m = folium.Map(location=map_center, zoom_start=15)
            
            # Add a marker for the searched address
            folium.Marker([latitude, longitude], tooltip="searched address", icon=folium.Icon(color='blue')).add_to(m)

            # Add markers for the businesses
            for data in business_data:
                folium.Marker(
                    [data['latitude'], data['longitude']],
                    tooltip=data['name'].lower(),
                    icon=folium.Icon(color='green')
                ).add_to(m)

            # Display the map
            st_folium(m, width=700, height=500)
        else:
            st.info("no businesses found within the specified distance.")

if __name__ == "__main__":
    main()
