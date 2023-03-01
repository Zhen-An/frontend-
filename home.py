import streamlit as st 
import pandas as pd 
import requests
import json

URL = "https://shielded-meadow-27035.herokuapp.com/air_sensor_records?per_page=100&direction=desc"
r = requests.request("GET", URL)
data=r.json()
df = pd.read_json(URL)
df = pd.json_normalize(data, record_path = ['records'])

st.sidebar.markdown('# Home')

header = st.container()
dataset = st.container()

with header: 
    st.title('IoT for Air Quality Monitoring')
    st.text('This page provides a table of the latest 100 records gathered from the PMS5003 sensor')

with dataset:
    st.subheader('Table of dataset') 
    st.table(df)
    st.write('Hi')





