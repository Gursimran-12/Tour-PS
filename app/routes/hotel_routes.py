from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)

from app.services.hotel_service import (
    search_hotels_service,
    nearby_places_service
)

hotel_bp = Blueprint(
    "hotel",
    __name__
)


# =====================================================
# Hotel Page
# =====================================================

@hotel_bp.route("/hotel")
def hotel():

    return render_template(
        "hotel.html"
    )


# =====================================================
# Search Hotels
# =====================================================

@hotel_bp.route("/search", methods=["POST"])
def search_hotels():

    try:

        data = request.get_json()

        result = search_hotels_service(
            data
        )

        return jsonify(result)

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# =====================================================
# Nearby Hotels / Restaurants
# =====================================================

@hotel_bp.route("/nearby")
def nearby():

    try:

        lat = request.args.get(
            "lat",
            type=float
        )

        lon = request.args.get(
            "lon",
            type=float
        )

        t_raw = request.args.get(
            "type",
            "restaurant"
        )

        radius_m = request.args.get(
            "radius_m",
            default=3000,
            type=int
        )

        if lat is None or lon is None:

            return jsonify({

                "error":
                    "lat and lon required"

            }), 400

        result = nearby_places_service(

            lat=lat,

            lon=lon,

            t_raw=t_raw,

            radius_m=radius_m
        )

        return jsonify(result)

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500