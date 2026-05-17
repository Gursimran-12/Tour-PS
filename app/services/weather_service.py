import requests

from flask import current_app

from app.utils.validators import (
    validate_coordinates
)

from app.utils.constants import (

    WEATHER_UNITS,

    DEFAULT_TIMEOUT
)


# =====================================================
# Fetch Current Weather
# =====================================================

def fetch_current_weather(
    lat,
    lon
):

    try:

        # =============================================
        # Validation
        # =============================================

        if not validate_coordinates(
            lat,
            lon
        ):

            return {

                "success": False,

                "error":
                    "Invalid coordinates"
            }

        # =============================================
        # OpenWeather API URL
        # =============================================

        url = (
            current_app.config[
                "WEATHER_BASE_URL"
            ]
            + "/weather"
        )

        params = {

            "lat":
                lat,

            "lon":
                lon,

            "appid":
                current_app.config[
                    "OPENWEATHER_KEY"
                ],

            "units":
                WEATHER_UNITS
        }

        # =============================================
        # API Request
        # =============================================

        response = requests.get(

            url,

            params=params,

            timeout=DEFAULT_TIMEOUT
        )

        response.raise_for_status()

        weather_data = response.json()

        # =============================================
        # Weather Formatting
        # =============================================

        result = {

            "success": True,

            "name":
                weather_data.get(
                    "name"
                ),

            "coord":
                weather_data.get(
                    "coord",
                    {}
                ),

            "temp_c":
                round(
                    weather_data[
                        "main"
                    ]["temp"]
                ),

            "feels_like_c":
                round(
                    weather_data[
                        "main"
                    ]["feels_like"]
                ),

            "humidity":
                weather_data[
                    "main"
                ]["humidity"],

            "wind_m_s":
                weather_data.get(
                    "wind",
                    {}
                ).get(
                    "speed"
                ),

            "condition":
                (
                    weather_data.get(
                        "weather"
                    )
                    or [{}]
                )[0].get(
                    "description"
                ),

            "icon":
                (
                    weather_data.get(
                        "weather"
                    )
                    or [{}]
                )[0].get(
                    "icon"
                )
        }

        return result

    except Exception as e:

        return {

            "success": False,

            "error":
                "weather_failed",

            "details":
                str(e)
        }


# =====================================================
# Weather Summary Helper
# =====================================================

def weather_summary(weather_data):

    if not weather_data.get(
        "success"
    ):

        return "Weather unavailable"

    return (

        f"{weather_data.get('condition', 'Unknown')} | "

        f"{weather_data.get('temp_c', '--')}°C | "

        f"Humidity: "
        f"{weather_data.get('humidity', '--')}%"
    )