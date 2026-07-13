import os
from wsgiref import headers
import requests
from dotenv import load_dotenv
from Utils.context import current_token
from Utils.helper import get_geo_location

load_dotenv()

WEATHER_API_KEY = os.getenv("weatherAPIKey")
VISUAL_CROSSING_API_KEY = os.getenv("visualCrossAPIKey")

WEATHER_API_URL = "https://api.weatherapi.com/v1/forecast.json"
VISUAL_CROSSING_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
ML_Weather_API_URL = "https://mlinfomap.org/weatherapi/get_weather"



    
def get_live_weather(location: str) -> dict:
    """
    Fetch live weather.

    Priority:
        1. ML_Weather_API_URL
        2. Visual Crossing (Fallback)
    """

    # -------------------------
    # WeatherAPI / ML_Weather_API_URL
    # -------------------------
    try:
        token = current_token.get()  # Retrieve the token from the context
        location_data = get_geo_location(location)
        loc = f"{location_data['lat']},{location_data['lon']}"

        response = requests.post(
            ML_Weather_API_URL,
            json={
                "q": loc,
            },
            headers={
                "Authorization": f"{token}"
            },
            timeout=10,
        )

        
        if response.status_code == 401:

            return {
                "success": False,
                "error": "UNAUTHORIZED",
                "message": "User session is revoked."
            }


        response.raise_for_status()
        response = normalize_weatherapi(response.json())

        return {
            "provider": "WeatherAPI",
            "success": True,
            "data": response
        }

    except requests.RequestException as weather_error:
        print(f"WeatherAPI Failed : {weather_error}")

    # -------------------------
    # Visual Crossing
    # -------------------------
    try:

        response = requests.get(
            f"{VISUAL_CROSSING_URL}/{location}",
            params={
                "unitGroup": "metric",
                "key": VISUAL_CROSSING_API_KEY,
                "contentType": "json",
            },
            timeout=10,
        )

        response.raise_for_status()

        return {
            "provider": "VisualCrossing",
            "success": True,
            "data": normalize_visualcrossing(response.json())
        }

    except requests.RequestException as visual_error:

        raise Exception(
            f"Both providers failed.\n"
            f"WeatherAPI Error: {weather_error}\n"
            f"Visual Crossing Error: {visual_error}"
        )
        
        
def normalize_weatherapi(data):

    return {
        "provider": "WeatherAPI",

        "location": {
            "name": data["location"]["name"],
            "region": data["location"]["region"],
            "country": data["location"]["country"],
            "latitude": data["location"]["lat"],
            "longitude": data["location"]["lon"],
            "timezone": data["location"]["tz_id"],
            "localtime": data["location"]["localtime"],
        },

        "current": {
            "temperature": data["current"]["temp_c"],
            "feels_like": data["current"]["feelslike_c"],
            "condition": data["current"]["condition"]["text"],
            "icon": data["current"]["condition"]["icon"],
            "humidity": data["current"]["humidity"],
            "pressure": data["current"]["pressure_mb"],
            "wind_speed": data["current"]["wind_kph"],
            "wind_direction": data["current"]["wind_dir"],
            "visibility": data["current"]["vis_km"],
            "uv": data["current"]["uv"],
            "cloud": data["current"]["cloud"],
            "precipitation": data["current"]["precip_mm"],
        },

        "air_quality": data["current"].get("air_quality", {}),

        "astronomy": data["forecast"]["forecastday"][0]["astro"],

        "alerts": data.get("alerts", {}).get("alert", []),

        "forecast": [
            {
                "date": d["date"],
                "condition": d["day"]["condition"]["text"],
                "max_temp": d["day"]["maxtemp_c"],
                "min_temp": d["day"]["mintemp_c"],
                "avg_temp": d["day"]["avgtemp_c"],
                "humidity": d["day"]["avghumidity"],
                "max_wind": d["day"]["maxwind_kph"],
                "rain_probability": d["day"]["daily_chance_of_rain"],
                "precipitation": d["day"]["totalprecip_mm"],
            }
            for d in data["forecast"]["forecastday"]
        ],
    }
    
    
    
def normalize_visualcrossing(data):

    today = data["days"][0]

    return {
        "provider": "VisualCrossing",

        "location": {
            "name": data.get("resolvedAddress"),
            "region": "",
            "country": "",
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "timezone": data["timezone"],
            "localtime": ""
        },

        "current": {
            "temperature": today["temp"],
            "feels_like": today["feelslike"],
            "condition": today["conditions"],
            "icon": today["icon"],
            "humidity": today["humidity"],
            "pressure": today["pressure"],
            "wind_speed": today["windspeed"],
            "wind_direction": today["winddir"],
            "visibility": today["visibility"],
            "uv": today["uvindex"],
            "cloud": today["cloudcover"],
            "precipitation": today["precip"],
        },

        "air_quality": {},

        "astronomy": {
            "sunrise": today["sunrise"],
            "sunset": today["sunset"],
            "moonrise": "",
            "moonset": "",
            "moon_phase": today["moonphase"],
        },

        "alerts": [],

        "forecast": [
            {
                "date": d["datetime"],
                "condition": d["conditions"],
                "max_temp": d["tempmax"],
                "min_temp": d["tempmin"],
                "avg_temp": d["temp"],
                "humidity": d["humidity"],
                "max_wind": d["windspeed"],
                "rain_probability": d["precipprob"],
                "precipitation": d["precip"],
            }
            for d in data["days"]
        ],
    }