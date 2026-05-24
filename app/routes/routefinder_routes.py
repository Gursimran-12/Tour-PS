from flask import (
    Blueprint,
    request,
    jsonify
)

import traceback

from app.utils.validators import (
    validate_coordinates,
    is_empty
)

from app.utils.constants import (
    DEFAULT_RADIUS_M,
    DEFAULT_PLACE_LIMIT
)

from app.services.geoapify_service import (
    geocode_location,
    extract_coordinates,
    get_route_between_points,
    reverse_geocode_service,
    fetch_nearby_places
)

from app.services.weather_service import (
    fetch_current_weather
)

routefinder_bp = Blueprint(
    "routefinder",
    __name__
)

# =====================================================
# Route API
# =====================================================

@routefinder_bp.route("/api/route")
def api_route():

    start = request.args.get("start")
    destination = request.args.get("destination")

    if is_empty(start) or is_empty(destination):

        return jsonify({
            "success": False,
            "error": "Missing start or destination"
        }), 400

    try:

# =================================================
# Safe India Bias
# =================================================

        if "india" not in start.lower():

            start_query = f"{start}, India"

        else:

            start_query = start

        if "india" not in destination.lower():

            destination_query = f"{destination}, India"

        else:

            destination_query = destination

        # =================================================
        # Geocode Start
        # =================================================

        start_geo = geocode_location(start_query)

        print("\n========== START GEO ==========")
        print(start_geo)

        if not start_geo.get("success"):

            return jsonify({
                "success": False,
                "error": "Start location not found"
            }), 404

        start_lat, start_lon = extract_coordinates(
            start_geo["data"]
        )

        if not validate_coordinates(
            start_lat,
            start_lon
        ):

            return jsonify({
                "success": False,
                "error": "Invalid start location"
            }), 404

        # =================================================
        # Geocode Destination
        # =================================================

        destination_geo = geocode_location(destination_query)

        print("\n========== DESTINATION GEO ==========")
        print(destination_geo)

        if not destination_geo.get("success"):

            return jsonify({
                "success": False,
                "error": "Destination not found"
            }), 404

        destination_lat, destination_lon = extract_coordinates(
            destination_geo["data"]
        )

        if not validate_coordinates(
            destination_lat,
            destination_lon
        ):

            return jsonify({
                "success": False,
                "error": "Invalid destination location"
            }), 404

        # =================================================
        # Car Route
        # =================================================

        route_result = get_route_between_points(

            start_lat,
            start_lon,

            destination_lat,
            destination_lon,

            mode="drive"
        )

        print("\n========== ROUTE RESULT ==========")
        print(route_result)

        if not route_result.get("success"):

            return jsonify({

                "success": False,

                "error":
                    "Route generation failed"

            }), 500

        route_data = route_result["data"]

        features = route_data.get(
            "features",
            []
        )

        if not features:

            return jsonify({

                "success": False,

                "error":
                    "No route found"

            }), 404

        properties = features[0].get(
            "properties",
            {}
        )

        distance_m = properties.get(
            "distance",
            0
        )

        time_s = properties.get(
            "time",
            0
        )

        distance_km = round(
            distance_m / 1000,
            2
        )

        drive_duration_hr = round(
            time_s / 3600,
            2
        )

        # =================================================
        # Weather
        # =================================================

        weather_result = fetch_current_weather(

            destination_lat,

            destination_lon
        )

        print("\n========== WEATHER ==========")
        print(weather_result)

        # =================================================
        # Modes
        # =================================================

        modes = [

            {

                "label": "Car",

                "distance_km":
                    distance_km,

                "duration_hr":
                    drive_duration_hr,

                "estimated_fare_inr":
                    round(distance_km * 12)
            },

            {

                "label": "Public Transport",

                "distance_km":
                    distance_km,

                "duration_hr":
                    round(drive_duration_hr * 1.5, 2),

                "estimated_fare_inr":
                    round(distance_km * 2.5)
            },

            {

                "label": "Bike",

                "distance_km":
                    distance_km,

                "duration_hr":
                    round(drive_duration_hr * 1.15, 2),

                "estimated_fare_inr":
                    round(distance_km * 4)
            },

            {

                "label": "Walk",

                "distance_km":
                    distance_km,

                "duration_hr":
                    round(distance_km / 5, 2),

                "estimated_fare_inr":
                    0
            }
        ]

        # =================================================
        # Formatted Address
        # =================================================

        formatted_start = (
            start_geo["data"]["features"][0]
            ["properties"]
            .get("formatted", start)
        )

        formatted_destination = (
            destination_geo["data"]["features"][0]
            ["properties"]
            .get("formatted", destination)
        )

        # =================================================
        # Final Response
        # =================================================

        response = {

            "success": True,

            "source": {

                "address": formatted_start
            },

            "destination": {

                "address": formatted_destination
            },

            "coordinates": {

                "start": {
                    "lat": start_lat,
                    "lon": start_lon
                },

                "destination": {
                    "lat": destination_lat,
                    "lon": destination_lon
                }
            },

            "modes": modes,

            "weather_at_destination": {

                "temperature_c":

                    weather_result.get(
                        "temp_c",
                        "--"
                    ),

                "description":

                    weather_result.get(
                        "condition",
                        "Unavailable"
                    ),

                "windspeed_m_s":

                    weather_result.get(
                        "wind_m_s",
                        "--"
                    )
            }
        }

        return jsonify(
            response
        )

    except Exception as e:

        print("\n========== FULL ERROR ==========")
        print(traceback.format_exc())

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500