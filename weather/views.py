from django.shortcuts import render
import json
import urllib.request
from datetime import datetime, timedelta

# Create your views here.

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        
        # OpenWeatherMap weather API endpoint
        weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=4016d60f1c430b22c895815fba65a8a2'
        res = urllib.request.urlopen(weather_url).read()
        
        # Decode bytes to string and then load the JSON data
        json_data = json.loads(res.decode('utf-8'))

        # Get coordinates
        lat = json_data['coord']['lat']
        lon = json_data['coord']['lon']
        
        # Convert temperature from Kelvin to Celsius
        temperature_in_celsius = json_data['main']['temp'] - 273.15
        
        # Fetch air quality data based on coordinates
        air_quality_url = f'https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid=4016d60f1c430b22c895815fba65a8a2'
        air_quality_res = urllib.request.urlopen(air_quality_url).read()
        air_quality_data = json.loads(air_quality_res.decode('utf-8'))
        
        # Extract air quality index
        air_quality = air_quality_data['list'][0]['main']['aqi']  # Air quality index
        
        # Get timezone offset from OpenWeatherMap's response (in seconds)
        timezone_offset = json_data['timezone']  # Timezone offset in seconds
        
        # Calculate local time based on the timezone offset (converting seconds to hours/minutes)
        local_time_utc = datetime.utcfromtimestamp(json_data['dt'])  # UTC time
        local_time = local_time_utc + timedelta(seconds=timezone_offset)  # Apply timezone offset
        local_time_str = local_time.strftime('%Y-%m-%d %H:%M:%S')  # Format local time as string
        
        data = {
            "country_code": str(json_data['sys']['country']),
            "coordinate": str(lat) + ', ' + str(lon),
            "temp": str(round(temperature_in_celsius, 2)) + '°C',  # rounded to 2 decimal places
            "pressure": str(json_data['main']['pressure']),
            "humidity": str(json_data['main']['humidity']),
            "air_quality": air_quality,  # Air quality index as an integer
            "local_time": local_time_str,  # Local time in human-readable format
        }
    else:
        city = ''
        data = {}

    return render(request, 'index.html', {'city': city, 'data': data})
