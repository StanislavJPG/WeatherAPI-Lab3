import json
import os

import requests
from math import floor
from dotenv import load_dotenv
from fastapi import FastAPI

# using FastAPI as framework because of it's simplicity
app = FastAPI(
    title='Weather'
)

load_dotenv()

@app.get('/api/weather/{city}')
def weather(city: str):
    # weather API url
    url = 'http://api.openweathermap.org/data/2.5/weather'
    # params with APPID and query
    weather_appid = os.environ.get('WeatherAPPID')
    parameters = {'q': city, 'APPID': weather_appid}

    # make GET request to url with all parameters
    response = requests.get(url, params=parameters)
    # transform response to json format
    weather = response.json()
    if response.status_code == 200:
        # text with i18n
        wind = weather['wind']
        try:
            weather_response: dict = {
                'City': city.title(),
                'Weather': weather['weather'][0]['description'],
                # set temperature as Celsius
                'Temperature': f'{floor(weather['main']['temp'] - 273.15)}°C',
                'Humidity': f'{weather['main']['humidity']}%',
                'Wind': {
                    'Speed': f'{wind.get('speed', None)} m/s',
                    'Degree': f'{wind.get('deg', None)}°',
                    'Max gust speed': f'{wind.get('gust', None)} m/s'
                }
            }
            # let's write result in txt file
            with open('weatherAPIdocs.txt', 'a') as file:
                file.write(json.dumps(weather_response) + '\n')
                file.close()

            return weather_response
        except KeyError:
            return {'Error': 'Oops. 500 error'}
    else:
        return {'Error': response.status_code}
