from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)

from app.services.geoapify_service import (
    reverse_geocode_service,
    fetch_nearby_places,
    get_route_between_points
)

from app.utils.validators import (
    validate_coordinates
)

findmyway_bp = Blueprint(
    "findmyway",
    __name__
)


# =====================================================
# FIND MY WAY PAGE
# =====================================================

@findmyway_bp.route("/findmyway")
def findmyway_view():

    return render_template(
        "findMyway.html"
    )


# =====================================================
# REVERSE GEOCODE
# =====================================================

@findmyway_bp.route(
    "/api/reverse",
    methods=["POST"]
)
def reverse_geocode():

    try:

        body = request.get_json(silent=True) or {}

        lat = body.get("lat")
        lng = body.get("lng")

        if lat is None or lng is None:

            return jsonify({

                "success": False,
                "error": "Latitude and Longitude required"

            }), 400

        lat = float(lat)
        lng = float(lng)

        if not validate_coordinates(lat, lng):

            return jsonify({

                "success": False,
                "error": "Invalid coordinates"

            }), 400

        result = reverse_geocode_service(
            lat,
            lng
        )

        if not result.get("success"):

            return jsonify({

                "success": False,
                "error": "Reverse geocoding failed"

            }), 500

        data = result.get(
            "data",
            {}
        )

        features = data.get(
            "features",
            []
        )

        if not features:

            return jsonify({

                "success": False,
                "error": "No address found"

            }), 404

        properties = features[0].get(
            "properties",
            {}
        )

        address = properties.get(
            "formatted",
            "Unknown location"
        )

        return jsonify({

            "success": True,
            "address": address

        })

    except Exception as e:

        return jsonify({

            "success": False,
            "error": str(e)

        }), 500


# =====================================================
# FETCH PLACES
# =====================================================

@findmyway_bp.route(
    "/api/places",
    methods=["POST"]
)
def places_api():

    try:

        body = request.get_json(silent=True) or {}

        lat = body.get("lat")
        lng = body.get("lng")

        if lat is None or lng is None:

            return jsonify({

                "success": False,
                "error": "Latitude and Longitude required"

            }), 400

        lat = float(lat)
        lng = float(lng)

        category = body.get(
            "category",
            "tourism.sights"
        )

        if not validate_coordinates(lat, lng):

            return jsonify({

                "success": False,
                "error": "Invalid coordinates"

            }), 400

        result = fetch_nearby_places(

            lat=lat,
            lon=lng,

            categories=category,

            radius_m=30000,

            limit=50
        )

        if not result.get("success"):

            return jsonify({

                "success": False,
                "error": "Places fetch failed"

            }), 500

        features = result["data"].get(
            "features",
            []
        )

        places = []

        for feature in features:

            properties = feature.get(
                "properties",
                {}
            )

            geometry = feature.get(
                "geometry",
                {}
            )

            coordinates = geometry.get(
                "coordinates",
                [None, None]
            )

            place_lon = coordinates[0]
            place_lat = coordinates[1]

            if not place_lat or not place_lon:
                continue

            places.append({

                "name":
                    properties.get(
                        "name",
                        "Unnamed"
                    ),

                "address":
                    properties.get(
                        "formatted",
                        ""
                    ),

                "lat": place_lat,
                "lng": place_lon,

                "distance_km":
                    round(
                        properties.get(
                            "distance",
                            0
                        ) / 1000,
                        2
                    )
            })

        return jsonify({

            "success": True,
            "places": places

        })

    except Exception as e:

        return jsonify({

            "success": False,
            "error": str(e)

        }), 500


# =====================================================
# ROUTE COORDINATES
# =====================================================

@findmyway_bp.route(
    "/api/route_coords",
    methods=["POST"]
)
def route_coords():

    try:

        body = request.get_json(silent=True) or {}

        src_lat = body.get("src_lat")
        src_lng = body.get("src_lng")

        dst_lat = body.get("dst_lat")
        dst_lng = body.get("dst_lng")

        if None in [src_lat, src_lng, dst_lat, dst_lng]:

            return jsonify({

                "success": False,
                "error": "All coordinates required"

            }), 400

        src_lat = float(src_lat)
        src_lng = float(src_lng)

        dst_lat = float(dst_lat)
        dst_lng = float(dst_lng)

        if not validate_coordinates(src_lat, src_lng):

            return jsonify({

                "success": False,
                "error": "Invalid source coordinates"

            }), 400

        if not validate_coordinates(dst_lat, dst_lng):

            return jsonify({

                "success": False,
                "error": "Invalid destination coordinates"

            }), 400

        transport_modes = [

            {
                "mode": "drive",
                "label": "Car"
            },

            {
                "mode": "walk",
                "label": "Walk"
            },

            {
                "mode": "bicycle",
                "label": "Bike"
            }
        ]

        all_routes = []

        for mode_data in transport_modes:

            route_result = get_route_between_points(

                src_lat,
                src_lng,

                dst_lat,
                dst_lng,

                mode=mode_data["mode"]
            )

            if not route_result.get("success"):
                continue

            route_data = route_result.get(
                "data",
                {}
            )

            features = route_data.get(
                "features",
                []
            )

            if not features:
                continue

            properties = features[0].get(
                "properties",
                {}
            )

            geometry = features[0].get("geometry")

            if not geometry:
                continue

            distance_m = properties.get(
                "distance",
                0
            )

            time_s = properties.get(
                "time",
                0
            )

            all_routes.append({

                "label":
                    mode_data["label"],

                "distance_km":
                    round(distance_m / 1000, 2),

                "duration_min":
                    round(time_s / 60),

                "estimated_fare_inr":
                    round((distance_m / 1000) * 12),

                "geometry":
                    geometry
            })

        # =========================================
        # PUBLIC TRANSPORT MOCK
        # =========================================

        if all_routes:

            all_routes.append({

                "label": "Public Transport",

                "distance_km":
                    all_routes[0]["distance_km"],

                "duration_min":
                    all_routes[0]["duration_min"] + 20,

                "estimated_fare_inr": 80,

                "geometry":
                    all_routes[0]["geometry"]
            })

        return jsonify({

            "success": True,
            "modes": all_routes

        })

    except Exception as e:

        return jsonify({

            "success": False,
            "error": str(e)

        }), 500

