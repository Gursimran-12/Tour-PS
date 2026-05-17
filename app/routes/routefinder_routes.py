from flask import (
    Blueprint,
    request,
    jsonify
)

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

    start = request.args.get(
        "start"
    )

    destination = request.args.get(
        "destination"
    )

    # =============================================
    # Validation
    # =============================================

    if is_empty(start) or is_empty(destination):

        return jsonify({

            "success": False,

            "error":
                "Missing start or destination"

        }), 400

    try:

        # =============================================
        # Geocode Start
        # =============================================

        start_geo = geocode_location(
            start
        )

        if not start_geo.get(
            "success"
        ):

            return jsonify({

                "success": False,

                "error":
                    "Start location not found"

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

                "error":
                    "Invalid start location"

            }), 404

        # =============================================
        # Geocode Destination
        # =============================================

        destination_geo = geocode_location(
            destination
        )

        if not destination_geo.get(
            "success"
        ):

            return jsonify({

                "success": False,

                "error":
                    "Destination not found"

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

                "error":
                    "Invalid destination location"

            }), 404

        # =============================================
        # Fetch Route
        # =============================================

        route_result = get_route_between_points(

            start_lat,
            start_lon,

            destination_lat,
            destination_lon
        )

        if not route_result.get(
            "success"
        ):

            return jsonify({

                "success": False,

                "error":
                    "Route generation failed"

            }), 500

        # =============================================
        # Route Formatting
        # =============================================

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

        # =============================================
        # Distance + Duration
        # =============================================

        distance_km = round(
            distance_m / 1000,
            2
        )

        drive_duration_hr = round(
            time_s / 3600,
            2
        )

        # =============================================
        # Weather
        # =============================================

        weather_result = fetch_current_weather(

            destination_lat,

            destination_lon
        )

        # =============================================
        # Transport Modes
        # =============================================

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

                "label": "Bus",

                "distance_km":
                    distance_km,

                "duration_hr":
                    round(drive_duration_hr * 1.4, 2),

                "estimated_fare_inr":
                    round(distance_km * 2.5)
            },

            {

                "label": "Bike",

                "distance_km":
                    distance_km,

                "duration_hr":
                    round(drive_duration_hr * 1.1, 2),

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

        # =============================================
        # Final Response
        # =============================================

        response = {

            "success": True,

            "source": {

                "address": start
            },

            "destination": {

                "address": destination
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

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# =====================================================
# Route Coordinates API
# =====================================================

@routefinder_bp.route("/api/route_coords")
def api_route_coords():

    start_lat = request.args.get(
        "start_lat",
        type=float
    )

    start_lon = request.args.get(
        "start_lon",
        type=float
    )

    destination_lat = request.args.get(
        "destination_lat",
        type=float
    )

    destination_lon = request.args.get(
        "destination_lon",
        type=float
    )

    # =============================================
    # Validation
    # =============================================

    if not validate_coordinates(
        start_lat,
        start_lon
    ):

        return jsonify({

            "success": False,

            "error":
                "Invalid start coordinates"

        }), 400

    if not validate_coordinates(
        destination_lat,
        destination_lon
    ):

        return jsonify({

            "success": False,

            "error":
                "Invalid destination coordinates"

        }), 400

    try:

        route_result = get_route_between_points(

            start_lat,
            start_lon,

            destination_lat,
            destination_lon
        )

        if not route_result.get(
            "success"
        ):

            return jsonify({

                "success": False,

                "error":
                    "Route generation failed"

            }), 500

        return jsonify(
            route_result["data"]
        )

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# =====================================================
# Nearby Places API
# =====================================================

@routefinder_bp.route("/api/places")
def api_places():

    lat = request.args.get(
        "lat",
        type=float
    )

    lon = request.args.get(
        "lon",
        type=float
    )

    category = request.args.get(
        "category",
        "tourism"
    )

    radius = request.args.get(
        "radius",
        default=DEFAULT_RADIUS_M,
        type=int
    )

    if not validate_coordinates(
        lat,
        lon
    ):

        return jsonify({

            "success": False,

            "error":
                "Invalid coordinates"

        }), 400

    try:

        result = fetch_nearby_places(

            lat=lat,

            lon=lon,

            categories=category,

            radius_m=radius,

            limit=DEFAULT_PLACE_LIMIT
        )

        if not result.get(
            "success"
        ):

            return jsonify({

                "success": False,

                "error":
                    "Places fetch failed"

            }), 500

        return jsonify(
            result["data"]
        )

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# =====================================================
# Reverse Geocoding API
# =====================================================

@routefinder_bp.route("/reverse_geocode")
def reverse_geocode():

    lat = request.args.get(
        "lat",
        type=float
    )

    lon = request.args.get(
        "lon",
        type=float
    )

    if not validate_coordinates(
        lat,
        lon
    ):

        return jsonify({

            "success": False,

            "error":
                "Invalid coordinates"

        }), 400

    try:

        result = reverse_geocode_service(
            lat,
            lon
        )

        if not result.get(
            "success"
        ):

            return jsonify({

                "success": False,

                "error":
                    "Reverse geocoding failed"

            }), 500

        return jsonify(
            result["data"]
        )

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500