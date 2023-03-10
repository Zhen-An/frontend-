import streamlit as st 
import pandas as pd 
import requests

st.sidebar.markdown('# Mask Guidance')

header = st.container()
advisory = st.container()
dataset = st.container()

URL1 = "https://shielded-meadow-27035.herokuapp.com/air_sensor_records?per_page=100&hours=1"
r = requests.request("GET", URL1)
data=r.json()
df1 = pd.read_json(URL1)
df1 = pd.json_normalize(data, record_path = ['records'])

URL24 = "https://shielded-meadow-27035.herokuapp.com/air_sensor_records?per_page=1500&hours=24"
r = requests.request("GET", URL24)
data=r.json()
df24 = pd.read_json(URL24)
df24 = pd.json_normalize(data, record_path = ['records'])

# This method takes PM2.5 concentration value as input and returns AQI value as output
def pm25_aqi(pm25):
    # Define breakpoints for PM2.5 concentration (ug/m3) and AQI
    c_low = [0, 12.1, 35.5, 55.5, 150.5, 250.5, 350.5]
    c_high = [12, 35.4, 55.4, 150.4, 250.4, 350.4, 500]
    i_low = [0, 51, 101, 151, 201, 301]
    i_high = [50 ,100 ,150 ,200 ,300 ,400]
  
   # Find the range where PM2.5 concentration falls
    for i in range(len(c_high)):
        if pm25 >= c_low[i] and pm25 <= c_high[i]:
            idx = i
  
   # Calculate AQI using linear interpolation formula
    aqi = ((i_high[idx] - i_low[idx]) / (c_high[idx] - c_low[idx])) * (pm25 - c_low[idx]) + i_low[idx]
  
   # Return AQI value rounded to integer
    return round(aqi)

columns2 = ['created', 'pm2d5', 'pm10']
df2 = df1[columns2]
df3 = df24[columns2]

df2['pm10'] = df2['pm10'].astype(float)
df2['pm2d5'] = df2['pm2d5'].astype(float)
df2['created'] = pd.to_datetime(df2['created'])

df3['pm10'] = df3['pm10'].astype(float)
df3['pm2d5'] = df3['pm2d5'].astype(float)
df3['created'] = pd.to_datetime(df3['created'])

avgaqi = df2['pm2d5'].mean()

with header: 
    st.title('Mask Guidance Advisory')
    st.text('This page will give advisory on whether you should continue to engage in your \nphysical activities and whether you should mask up based on your health profile')

with advisory:
    st.header('Health Advisory')
    AQI = pm25_aqi(avgaqi)
    lastvalue = int(df2['pm2d5'].iloc[-1])
    deviation = AQI - lastvalue 
    st.metric("Air Quality Index", AQI, deviation)

    age = st.number_input('Enter your age', step = 1)
    healthcondition = st.selectbox('Enter your health profile', ['Healthy', 'Lung Conditions', 'Heart Conditions'])
    group = 0
    if age <= 17 or age >= 65 or healthcondition != 'Healthy':
        group = 1
        st.write('You belong in the sensitive group.')
    else:
        st.write('You belong in the normal group.')

    if 0 <= AQI <= 50:
        st.write('Air Quality Index is Good.')
        st.write('It is a great day to be active outside.') 

    elif 51 <= AQI <= 100:
        st.write('Air Quality Index is Moderate.')
        if group == 1:
            st.write('Consider reducing prolonged or heavy exertion. Watch for symptons such as coughing or shortness of breath. These are signs to take it easier.') 
        else:
            st.write('It is a good day to be active outside.')

    elif 101 <= AQI <= 150:
        st.write('Air Quality Index is Unhealthy for Sensitive Group.')
        if group == 1:
            st.write('Reduced prolonged or heavy exertion. It is OK to be active outside, but take more breaks and do less intense activities. Watch for symptoms such as coughing or shortness of breath.')
        else:
            st.write('It is a good day to be active outside.')

    elif 151 <= AQI <= 200:
        st.write('Air Quality Index is Unhealthy.')
        if group == 1: 
            st.write('Avoid prolinged or heavy exertion. More activities indoors or reschedule to a time when the air qaulity is better.')
        else:
            st.write('Reduce prolonged or heavy exertion. Take more breaks during all outdoor activities.')
    
    elif 201 <= AQI <= 300:
        st.write('Air Quality Index is Very Unhealthy.')
        if group == 1:
            st.write('Avoid all physical activites outdoors. More activities indoors or reschedule to a time when air quality is better.')
        else:
            st.write('Avoid prolonged or heavy exertion. Consider moving activities indoor or rescheduling to a time when air quality is better.')
        
    else:
        st.write('Air Quality Index is Hazardous.')
        if group == 1:
            st.write('Remain indoors and keep activity levels low. Follow tips for keeping particle levels low indoors.')
        else:
            st.write('Avoid all physical activity outdoors.')

with dataset:
     st.subheader('Trendline for both PM2.5 and PM10 datas for the past 24 hours')
     st.line_chart(df3, x='created', y=['pm10', 'pm2d5'])

with dataset: 
    st.subheader('Trendline for both PM2.5 and PM10 datas for the past hour')
    st.table(df2)
    st.line_chart(df2, x='created', y=['pm2d5', 'pm10'])


    


    


    