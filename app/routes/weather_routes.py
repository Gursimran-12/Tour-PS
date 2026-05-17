from flask import (
    Blueprint,
    jsonify,
    request
)

from app.services.weather_service import (
    fetch_current_weather
)

weather_bp = Blueprint(
    "weather",
    __name__
)


# =====================================================
# Current Weather API
# =====================================================

@weather_bp.route("/api/weather_current")
def api_weather_current():

    try:

        lat = request.args.get(
            "lat",
            type=float
        )

        lon = request.args.get(
            "lon",
            type=float
        )

        result = fetch_current_weather(
            lat,
            lon
        )

        status_code = 200

        if not result.get("success"):

            status_code = 500

        return jsonify(result), status_code

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500