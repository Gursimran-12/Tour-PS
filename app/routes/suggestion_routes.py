from flask import (
    Blueprint,
    request,
    jsonify,
    current_app
)

import pandas as pd

from app.utils.validators import (
    is_empty
)

from app.utils.constants import (
    DEFAULT_PLACE_LIMIT
)

from app.services.budget_service import (
    generate_budget_plan
)

from app.services.geoapify_service import (

    geocode_location,

    extract_coordinates,

    fetch_nearby_places,

    normalize_places
)

suggestion_bp = Blueprint(
    "suggestion",
    __name__
)


# =====================================================
# Suggest Places
# =====================================================

@suggestion_bp.route("/suggest")
def suggest():

    try:

        query = request.args.get(
            "query",
            ""
        ).strip().lower()

        # =============================================
        # Validation
        # =============================================

        if is_empty(query):

            return jsonify([])

        # =============================================
        # Load Dataset
        # =============================================

        df = pd.read_csv(

            current_app.config[
                "PLACES_DATASET"
            ]
        )

        # =============================================
        # Filter Suggestions
        # =============================================

        suggestions = []

        for col in df.columns:

            values = df[col].astype(
                str
            )

            matches = values[
                values.str.lower().str.contains(
                    query,
                    na=False
                )
            ].unique()

            for m in matches:

                if (
                    str(m).strip()
                    and str(m) not in suggestions
                ):

                    suggestions.append(
                        str(m)
                    )

        # =============================================
        # Limit Suggestions
        # =============================================

        suggestions = suggestions[
            :DEFAULT_PLACE_LIMIT
        ]

        return jsonify(
            suggestions
        )

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# =====================================================
# Geo Suggestions
# =====================================================

@suggestion_bp.route(
    "/suggest_geo",
    methods=["POST"]
)
def suggest_geo():

    try:

        data = request.get_json() or {}

        state = data.get(
            "state",
            ""
        ).strip()

        category = data.get(
            "category",
            ""
        ).strip().lower()

        # =============================================
        # Validation
        # =============================================

        if is_empty(state) or is_empty(category):

            return jsonify({

                "success": False,

                "error":
                    "State and category are required"

            }), 400

        # =============================================
        # Geocode State
        # =============================================

        geo_result = geocode_location(
            state
        )

        if not geo_result.get(
            "success"
        ):

            return jsonify({

                "success": False,

                "error":
                    "Location not found"

            }), 404

        lat, lon = extract_coordinates(
            geo_result["data"]
        )

        if lat is None or lon is None:

            return jsonify({

                "success": False,

                "error":
                    "Coordinates not found"

            }), 404

        # =============================================
        # Category Mapping
        # =============================================

        category_map = {

            "historical":
                "tourism.sights",

            "religious":
                "religion",

            "museum":
                "entertainment.museum",

            "heritage":
                "tourism",

            "leisure":
                "leisure",

            "nature":
                "natural"
        }

        geo_category = category_map.get(

            category,

            "tourism.sights"
        )

        # =============================================
        # Fetch Nearby Places
        # =============================================

        places_result = fetch_nearby_places(

            lat=lat,

            lon=lon,

            categories=geo_category,

            radius_m=50000,

            limit=20
        )

        if not places_result.get(
            "success"
        ):

            return jsonify({

                "success": False,

                "error":
                    "Failed to fetch places"

            }), 500

        features = places_result[
            "data"
        ].get(
            "features",
            []
        )

        normalized_places = normalize_places(
            features
        )

        return jsonify({

            "success": True,

            "places":
                normalized_places

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500

        # =============================================
        # Format Places
        # =============================================

        places = []

        for item in result.get(
            "results",
            []
        ):

            places.append({

                "name":
                    item.get(
                        "formatted",
                        "Unknown Place"
                    ),

                "category":
                    category,

                "address":
                    item.get(
                        "formatted",
                        ""
                    ),

                "lat":
                    item.get(
                        "lat"
                    ),

                "lon":
                    item.get(
                        "lon"
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

        # =============================================
        # Validation
        # =============================================

        if is_empty(text):

            return jsonify([])

        # =============================================
        # Geoapify Autocomplete Service
        # =============================================

        result = autocomplete_places(

            text=text,

            limit=DEFAULT_PLACE_LIMIT
        )

        if not result.get(
            "success"
        ):

            return jsonify({

                "success": False,

                "error":
                    result.get(
                        "error",
                        "Autocomplete failed"
                    )

            }), 500

        return jsonify(
            result.get(
                "results",
                []
            )
        )

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# =====================================================
# Generate Budget Plan
# =====================================================

@suggestion_bp.route(
    "/generate_plan",
    methods=["POST"]
)
def generate_plan():

    try:

        data = request.get_json()

        # =============================================
        # Validation
        # =============================================

        if not data:

            return jsonify({

                "success": False,

                "error":
                    "Request body is missing"

            }), 400

        # =============================================
        # Generate Plan
        # =============================================

        result = generate_budget_plan(
            data
        )

        return jsonify(result)

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500