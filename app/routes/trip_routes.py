from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    current_app,
    jsonify
)

from app.services.geoapify_service import (
    geocode_location,
    extract_coordinates,
    fetch_nearby_places,
    reverse_geocode_service
)

trip_bp = Blueprint(
    "trip",
    __name__
)


# =====================================================
# Landing Page
# =====================================================

@trip_bp.route("/")
def landing():

    return render_template(
        "index.html"
    )


# =====================================================
# Home Page
# =====================================================

@trip_bp.route("/home")
def home_page():

    if "username" not in session:

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "home.html"
    )


# =====================================================
# Information Page
# =====================================================

@trip_bp.route("/information")
def information():

    return render_template(
        "information.html",
        GEOAPIFY_KEY=current_app.config[
            "GEOAPIFY_KEY"
        ]
    )


# =====================================================
# Generate Page
# =====================================================

@trip_bp.route("/generate")
def generate():

    q = request.args

    city = (
        q.get("city") or ""
    ).strip()

    state = (
        q.get("state") or ""
    ).strip()

    days = int(
        q.get("days") or 1
    )

    start_time = (
        q.get("start") or "09:00"
    ).strip()

    stop_time = (
        q.get("stop") or "18:00"
    ).strip()

    categories_csv = (
        q.get("categories") or ""
    ).strip()

    categories = [

        c for c in categories_csv.split(",")

        if c
    ]

    # =================================================
    # Prefer lat/lon from frontend
    # =================================================

    lat = q.get("lat")

    lon = q.get("lon")

    # =================================================
    # Geocode if lat/lon missing
    # =================================================

    if not lat or not lon:

        if not city or not state:

            return redirect(
                url_for("trip.information")
            )

        try:

            geo = geocode_location(
                f"{city}, {state}"
            )

            if not geo.get("success"):

                return redirect(
                    url_for("trip.information")
                )

            lat, lon = extract_coordinates(
                geo["data"]
            )

            if lat is None or lon is None:

                return redirect(
                    url_for("trip.information")
                )

        except Exception:

            return redirect(
                url_for("trip.information")
            )

    # =================================================
    # Normalize Coordinates
    # =================================================

    try:

        lat = float(lat)

        lon = float(lon)

    except Exception:

        return redirect(
            url_for("trip.information")
        )

    # =================================================
    # Render Generate Page
    # =================================================

    return render_template(

        "generate.html",

        city=city,

        state=state,

        days=days,

        start_time=start_time,

        stop_time=stop_time,

        categories=categories,

        lat=lat,

        lon=lon,
        
    )


# =====================================================
# Trip Schedule Page
# =====================================================

@trip_bp.route("/trip_schedule")
def schedule_view():

    return render_template(
        "trip_schedule.html"
    )


# =====================================================
# Budget Management Page
# =====================================================

@trip_bp.route("/budget_management")
def budget_management():

    return render_template(
        "budget_management.html"
    )


# =====================================================
# Tips Page
# =====================================================

@trip_bp.route("/tips")
def tips_page():

    return render_template(
        "tips.html"
    )


# =====================================================
# Sightseeing Suggestion Page
# =====================================================

@trip_bp.route("/sightseeing_suggestion")
def sightseeing():

    return render_template(
        "sightseeing_suggestion.html"
    )


# =====================================================
# Hotel Page
# =====================================================

@trip_bp.route("/hotel")
def hotel():

    return render_template(
        "hotel.html"
    )


# =====================================================
# About Us Page
# =====================================================

@trip_bp.route("/AboutUs")
def AboutUs():

    return render_template(
        "AboutUs.html"
    )


# =====================================================
# Find My Way Page
# =====================================================

@trip_bp.route("/findmyway")
def findmyway_view():

    return render_template(
        "findMyway.html"
    )


# =====================================================
# Route Finder Page
# =====================================================

@trip_bp.route("/routefinder")
def routefinder_page():

    return render_template(
        "routefinder.html"
    )


# =====================================================
# Dynamic Planner Page
# =====================================================

@trip_bp.route("/dynamic")
def serve_dynamic():

    return render_template(
        "dynamic.html"
    )

# =====================================================
# Nearby Places API
# =====================================================

@trip_bp.route("/api/nearby_places")
def nearby_places():

    try:

        lat = request.args.get(
            "lat",
            type=float
        )

        lon = request.args.get(
            "lon",
            type=float
        )

        radius = request.args.get(
            "radius",
            default=3000,
            type=int
        )

        category = request.args.get(
            "category"
        )

        result = fetch_nearby_places(

            lat=lat,

            lon=lon,

            categories=category,

            radius_m=radius,

            limit=30
        )

        if not result.get("success"):

            return jsonify(result), 500

        return jsonify({

            "success": True,

            "features":
                result["data"].get(
                    "features",
                    []
                )

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500

@trip_bp.route("/dynamic.html")
def serve_dynamic_html_file():

    return render_template(
        "dynamic.html"
    )
    
    # =====================================================
# Reverse Geocode API
# =====================================================

@trip_bp.route("/reverse_geocode")
def reverse_geocode():

    lat = request.args.get(
        "lat",
        type=float
    )

    lon = request.args.get(
        "lon",
        type=float
    )

    if lat is None or lon is None:

        return jsonify({

            "error":
                "Latitude and Longitude required"

        }), 400

    result = reverse_geocode_service(
        lat,
        lon
    )

    if not result.get("success"):

        return jsonify({

            "error":
                result.get("error")

        }), 500

    return jsonify(
        result["data"]
    )