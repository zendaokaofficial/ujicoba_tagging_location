import streamlit as st
import geocoder
from shapely.geometry import Point, MultiPoint, MultiPolygon
import pandas as pd

st.title("Tag Multiple GPS Locations to Create a MultiPolygon")

# Sidebar input for tagging
st.sidebar.markdown("Tag your GPS locations:")

# Initialize a list to store the tagged locations
tagged_locations = []

# Button to get the current location
if st.sidebar.button("Get Current Location"):
    location = geocoder.ip("me")

    if location:
        latitude = round(location.latlng[0], 7)  # Round latitude to 7 decimal places
        longitude = round(location.latlng[1], 7)  # Round longitude to 7 decimal places

        # Store the tagged location as a Point
        point = Point(longitude, latitude)
        tagged_locations.append(point)

        st.success(f"Location tagged at Latitude: {latitude}, Longitude: {longitude}")
    else:
        st.warning("Unable to retrieve your current location. Please check your internet connection.")

# Display tagged locations
st.sidebar.title("Tagged Locations")

if tagged_locations:
    st.sidebar.markdown("Tagged Locations:")
    location_table = pd.DataFrame(
        {
            "Latitude": [f"{point.y:.7f}" for point in tagged_locations],  # Format to 7 decimal places
            "Longitude": [f"{point.x:.7f}" for point in tagged_locations],  # Format to 7 decimal places
        }
    )
    st.sidebar.dataframe(location_table)

# Button to create a MultiPolygon
if st.sidebar.button("Create MultiPolygon"):
    if tagged_locations:
        multi_point = MultiPoint(tagged_locations)
        multi_polygon = multi_point.convex_hull

        # You can save the MultiPolygon to a file or perform other actions here.
        st.success("MultiPolygon created.")

# Display the MultiPolygon
if "multi_polygon" in st.session_state:
    st.markdown("### MultiPolygon:")
    st.write(st.session_state.multi_polygon)
