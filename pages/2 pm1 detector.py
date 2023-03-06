import streamlit as st 
import pandas as pd 
import requests
from bs4 import BeautifulSoup
import telegram
import time 

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

# Set up the Telegram bot
bot = telegram.Bot(token='6263023646:AAGazIM4dn0eRPh1TEUcOzXhrMmb6Atv8rw')

# Define the Streamlit app URL
url = 'https://zhen-an-frontend--home-mqw6sn.streamlit.app/pm1_detector'

# Define the initial value
initial_value = 0

while True:
    # Fetch the Streamlit app HTML
    response = requests.get(url)
    html = response.content

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Extract the value of interest
    value = soup.find('div', {'class': 'streamlit-metric'}).get('aria-valuenow')

    # Convert the value to a number
    value = float(value)

    # Check for changes
    if value != initial_value:
        # Send a message to the Telegram bot
        bot.send_message(chat_id='-1001872135066', text=f'The PM1 value has changed to {value}!')

        # Update the initial value
        initial_value = value

    # Wait for some time before checking again
    time.sleep(60)
