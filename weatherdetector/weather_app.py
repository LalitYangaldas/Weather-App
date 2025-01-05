import streamlit as st
import requests
from datetime import datetime, timedelta

# Function to get weather and air quality data
def get_weather_data(city):
    # Replace with your OpenWeatherMap API key
    api_key = '4016d60f1c430b22c895815fba65a8a2'
    
    # OpenWeatherMap weather endpoint
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    weather_response = requests.get(weather_url).json()
    
    # OpenWeatherMap air quality endpoint
    lat = weather_response['coord']['lat']
    lon = weather_response['coord']['lon']
    
    air_quality_url = f'https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
    air_quality_response = requests.get(air_quality_url).json()
    
    # Get weather data
    temperature_in_celsius = weather_response['main']['temp'] - 273.15
    pressure = weather_response['main']['pressure']
    humidity = weather_response['main']['humidity']
    
    # Get air quality data (AQI)
    air_quality = air_quality_response['list'][0]['main']['aqi']
    
    # Calculate local time
    timezone_offset = weather_response['timezone']
    local_time_utc = datetime.utcfromtimestamp(weather_response['dt'])
    local_time = local_time_utc + timedelta(seconds=timezone_offset)
    local_time_str = local_time.strftime('%Y-%m-%d %H:%M:%S')
    
    # Return the results
    return {
        "country_code": weather_response['sys']['country'],
        "coordinates": f"{lat}, {lon}",
        "temperature": f"{round(temperature_in_celsius, 2)}°C",
        "pressure": pressure,
        "humidity": humidity,
        "air_quality": air_quality,
        "local_time": local_time_str
    }

# Streamlit app UI
st.title('Weather App')

# Input for city name
city = st.text_input('Enter city name:', 'London')

if city:
    # Get the weather data
    data = get_weather_data(city)
    
    # Display the data
    st.subheader(f"Weather in {city}, {data['country_code']}")
    st.write(f"Coordinates: {data['coordinates']}")
    st.write(f"Temperature: {data['temperature']}")
    st.write(f"Pressure: {data['pressure']} hPa")
    st.write(f"Humidity: {data['humidity']} %")
    st.write(f"Air Quality Index: {data['air_quality']}")
    st.write(f"Local Time: {data['local_time']}")
