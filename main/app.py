import streamlit as st
from queries import find_businesses_within_distance
from geocode import geocode_address

def main():
    st.title("welcome to neighbrhood")

    # Input for address
    address = st.text_input("enter your address:")
    
    # Input for distance
    distance = st.number_input("enter distance in meters:", min_value=0, value=100, step=1)

    # When the user clicks the button, geocode the address and find businesses
    if st.button("search"):
        if address:
            latitude, longitude = geocode_address(address)
            if latitude is None or longitude is None:
                st.error("could not geocode the address. please try again.")
            else:
                businesses = find_businesses_within_distance(latitude, longitude, distance)
                if businesses:
                    st.success(f"businesses within {distance:.2f} meters of '{address}':")
                    for business in businesses:
                        st.write(f"- {business[0]}")
                else:
                    st.info("no businesses found within the specified distance.")
        else:
            st.warning("please enter an address.")

if __name__ == "__main__":
    main()
