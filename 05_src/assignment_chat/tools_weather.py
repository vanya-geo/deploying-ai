from langchain.tools import tool
import json
import requests

@tool
def get_weather_tool(query: str):
    """
    Retrieves latitude/longitude and current weather for a location.
    Returns a formatted string summary of the weather.
    """

    # --- Geocoding ---
    geo_response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": query, "count": 1, "language": "en", "format": "json"},
        timeout=20
    )
    geo_response.raise_for_status()
    geo = geo_response.json()

    if "results" not in geo or len(geo["results"]) == 0:
        return f"Location '{query}' not found."

    location = geo["results"][0]["name"]
    country = geo["results"][0].get("country", "")
    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]

    # --- Weather Request ---
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ",".join([
            "temperature_2m",
            "apparent_temperature",
            "relative_humidity_2m",
            "precipitation",
            "rain",
            "showers",
            "snowfall",
            "cloud_cover",
            "wind_speed_10m",
            "wind_gusts_10m",
            "wind_direction_10m",
            "surface_pressure",
            "visibility",
            "uv_index",
            "weather_code"
        ]),
        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh",
        "precipitation_unit": "mm",
        "timezone": "auto"
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    if "current" not in data:
        return f"Weather data unavailable for {location}."

    current = data["current"]

    # --- Format Output String ---
    weather_summary = (
        f"Current weather in {location}, {country}:\n"
        f"Temperature: {current.get('temperature_2m')}°C\n"
        f"Feels like: {current.get('apparent_temperature')}°C\n"
        f"Humidity: {current.get('relative_humidity_2m')}%\n"
        f"Precipitation: {current.get('precipitation')} mm\n"
        f"Rain: {current.get('rain')} mm\n"
        f"Snowfall: {current.get('snowfall')} mm\n"
        f"Cloud cover: {current.get('cloud_cover')}%\n"
        f"Wind speed: {current.get('wind_speed_10m')} km/h\n"
        f"Wind gusts: {current.get('wind_gusts_10m')} km/h\n"
        f"Wind direction: {current.get('wind_direction_10m')}°\n"
        f"Pressure: {current.get('surface_pressure')} hPa\n"
        f"Visibility: {current.get('visibility')} m\n"
        f"UV Index: {current.get('uv_index')}\n"
        f"Weather code: {current.get('weather_code')}"
    )

    return weather_summary