import streamlit as st 
import pandas as pd 
import requests
import json

st.sidebar.markdown('# PM 1 Detector')

header = st.container()
advisory = st.container()

URL = "https://shielded-meadow-27035.herokuapp.com/air_sensor_records"
r = requests.request("GET", URL)
data=r.json()
df = pd.read_json(URL)
df = pd.json_normalize(data, record_path = ['records'])

with header:
    st.title('PM1 Detector')
    st.write('This page detects particles with less than 1 micrometer')
    st.write('Our lungs are prey to PM1. When inhaled, PM1 particles travel to the deepest area of the lungs, where a significant part of them passes through the cell membranes of the alveoli (the millions of tiny sacs in our lungs where O2 and CO2 are exchanged), enter the bloodstream, damage the inner walls of arteries, penetrate tissue in the cardiovascular system and potentially spread to organs.')
    st.write('At worst, PM1 can contribute to deadly diseases like heart attacks, lung cancer, dementia, emphysema, edema and other serious disease, leading to premature death.')

with advisory:
    columns1 = ['created', 'pm1']
    df1 = df[columns1]
    df1['pm1'] = df1['pm1'].astype(float)
    st.table(df1)
    avgpm1 = df1['pm1'].mean()
    lastvalue = float(df1['pm1'].iloc[-1])
    deviation = avgpm1 - lastvalue 
    st.title('PM1 Value & Deviation')
    st.metric('PM1', avgpm1, deviation)