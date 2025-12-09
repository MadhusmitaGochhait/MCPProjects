import requests
import re
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv
import os

load_dotenv(override=True)
API_KEY = os.getenv("WEATHER_API_KEY")

def geocode_location(location: str):
   # WeatherAPI supports direct location query, no separate geocoding
    return location  # we can pass location name directly!



def fetch_current_weather(location: str):
    url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": API_KEY,
        "q": location,
        "aqi": "no"
    }
    r = requests.get(url, params=params).json()

    try:
        loc = r["location"]["name"]
        temp = r["current"]["temp_c"]
        condition = r["current"]["condition"]["text"]
        wind = r["current"]["wind_kph"]
        return f"{temp}°C, {condition}, wind {wind} km/h"
    except:
        return "Weather data not available."
# -------- 3. Weather by date (forecast) ----------
def fetch_weather_on_date(location: str, date: datetime = None):
    url = "https://api.weatherapi.com/v1/forecast.json"
    date_str = date.strftime("%Y-%m-%d")
    params = {
        "key": API_KEY,
        "q": location,
        "dt": date_str,
    }

    r = requests.get(url, params=params).json()

    try:
        day = r["forecast"]["forecastday"][0]["day"]
        max_t = day["maxtemp_c"]
        min_t = day["mintemp_c"]
        condition = day["condition"]["text"]
        return f"{max_t}°C / {min_t}°C, {condition}"
    except:
        return "Forecast not available."