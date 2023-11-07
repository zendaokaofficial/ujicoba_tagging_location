# app.py

import streamlit as st
import geocoder
from shapely.geometry import Point, MultiPoint, MultiPolygon
import pandas as pd

st.title("Tag Multiple GPS Locations to Create a MultiPolygon")

# Initialize session state to store tagged locations
if "tagged_locations" not in st.session_state:
    st.session_state.tagged_locations = []

# Sidebar input for tagging
st.sidebar.markdown("Tag your GPS locations:")

# Button to get the current location
if st.sidebar.button("Get Current Location"):
    location = geocoder.ip("me")

    if location:
        latitude = location.latlng[0]
        longitude = location.latlng[1]

        # Store the tagged location as a Point
        point = Point(longitude, latitude)
        st.session_state.tagged_locations.append(point)

        st.success(f"Location tagged at Latitude: {latitude}, Longitude: {longitude}")
    else:
        st.warning("Unable to retrieve your current location. Please check your internet connection.")

# Display tagged locations
st.sidebar.title("Tagged Locations")

if st.session_state.tagged_locations:
    st.sidebar.markdown("Tagged Locations:")
    location_table = pd.DataFrame(
        {
            "Latitude": [point.y for point in st.session_state.tagged_locations],
            "Longitude": [point.x for point in st.session_state.tagged_locations],
        }
    )
    st.sidebar.dataframe(location_table)

# Button to create a MultiPolygon
if st.sidebar.button("Create MultiPolygon"):
    if st.session_state.tagged_locations:
        multi_point = MultiPoint(st.session_state.tagged_locations)
        multi_polygon = multi_point.convex_hull

        # Store the MultiPolygon in session state
        st.session_state.multi_polygon = multi_polygon
        st.success("MultiPolygon created.")

# Display the MultiPolygon
if "multi_polygon" in st.session_state:
    st.markdown("### MultiPolygon:")
    st.write(st.session_state.multi_polygon)
