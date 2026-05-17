from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)

from app.services.review_service import (
    fetch_place_reviews
)

review_bp = Blueprint(
    "review",
    __name__
)


# =====================================================
# Fetch Reviews
# =====================================================

@review_bp.route(
    "/reviews",
    methods=["POST"]
)
def reviews():

    try:

        body = request.get_json() or {}

        result = fetch_place_reviews(

            name=body.get(
                "name"
            ),

            address=body.get(
                "address"
            ),

            lat=body.get(
                "lat"
            ),

            lon=body.get(
                "lon"
            )
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


# =====================================================
# Reviews Page
# =====================================================

@review_bp.route("/hotels_reviews")
def hotels_reviews_view():

    return render_template(
        "hotels_reviews.html"
    )


@review_bp.route("/hotels_reviews.html")
def hotels_reviews_html():

    return render_template(
        "hotels_reviews.html"
    )