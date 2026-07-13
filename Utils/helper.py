import requests
import os
from dotenv import load_dotenv



load_dotenv()
MAPTILER_API_KEY = os.getenv("maptilerAPIKey")

# To Get the lat/lon of a location
def get_geo_location(location: str):
    url = f"https://api.maptiler.com/geocoding/{location}.json"

    response = requests.get(
        url,
        params={
            "key": MAPTILER_API_KEY,
            "country": "in",
            "language": "en",
            "limit": 1
        },
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if not data["features"]:
        raise ValueError(f"No location found for '{location}'")

    # MapTiler returns [longitude, latitude]
    lon, lat = data["features"][0]["center"]
    return  {
        "lat": lat,
        "lon": lon
    }
