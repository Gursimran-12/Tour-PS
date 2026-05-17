from flask import Blueprint, request, jsonify
import requests

location_bp = Blueprint("location", __name__)


# =========================================================
# REVERSE GEOCODE
# Convert latitude + longitude -> place name
# =========================================================

@location_bp.route("/reverse_geocode", methods=["GET"])
def reverse_geocode():

    lat = request.args.get("lat")
    lon = request.args.get("lon")

    try:

        url = (
            f"https://nominatim.openstreetmap.org/reverse"
            f"?format=jsonv2&lat={lat}&lon={lon}"
        )

        headers = {
            "User-Agent": "TravelPlannerApp"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        data = response.json()

        address = data.get("address", {})

        city = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or ""
        )

        state = address.get("state", "")

        country = address.get("country", "")

        formatted = ", ".join(
            [x for x in [city, state, country] if x]
        )

        return jsonify({
            "formatted": formatted
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# GEOCODE LOCATION
# Convert city + state -> latitude longitude
# =========================================================

@location_bp.route("/geocode_location", methods=["GET"])
def geocode_location():

    city = request.args.get("city")
    state = request.args.get("state")

    try:

        if not city or not state:

            return jsonify({
                "error": "City and state are required"
            }), 400

        query = f"{city}, {state}, India"

        url = (
            "https://nominatim.openstreetmap.org/search"
        )

        params = {
            "q": query,
            "format": "jsonv2",
            "limit": 1
        }

        headers = {
            "User-Agent": "TravelPlannerApp"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        data = response.json()

        if not data or len(data) == 0:

            return jsonify({
                "error": "Location not found"
            }), 404

        place = data[0]

        lat = float(place["lat"])
        lon = float(place["lon"])

        display_name = place.get(
            "display_name",
            query
        )

        return jsonify({

            "lat": lat,

            "lon": lon,

            "formatted": display_name

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500