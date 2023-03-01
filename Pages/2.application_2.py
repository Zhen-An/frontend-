import streamlit as st 
import pandas as pd 
import requests
import json

URL = "https://shielded-meadow-27035.herokuapp.com/air_sensor_records"
r = requests.request("GET", URL)
data=r.json()
df = pd.read_json(URL)
df = pd.json_normalize(data, record_path = ['records'])

st.sidebar.markdown('# Application 2')
