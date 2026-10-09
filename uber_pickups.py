# Import required libraries
import streamlit as st
import pandas as pd
import numpy as np

# Set the application title
st.title('Uber pickups in NYC')

# Define the dataset URL and date/time column
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# Load, prepare and cache the Uber pickups dataset
@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Display the data-loading status
data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text('Loading data...done!')


# Add a checkbox to let users choose whether to view the raw data
if st.checkbox('Show raw data'):

    # Display the dataset only when the checkbox is selected
    st.subheader('Raw data')
    st.write(data)


# Display a heading for the hourly pickup histogram
st.subheader('Number of pickups by hour')

# Count Uber pickups for each hour of the day (0–23)
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24)
)[0]

# Display the hourly pickup counts as a bar chart
st.bar_chart(hist_values)


# Allow users to select an hour of the day
hour_to_filter = st.slider('hour', 0, 23, 17)

# Display the selected hour above the map
st.subheader('Map of all pickups at %s:00' % hour_to_filter)

# Show only pickups recorded during the selected hour
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# Plot the filtered pickup locations
st.map(filtered_data)
