from flask import (
    Blueprint,
    request,
    jsonify
)

from app.services.schedule_service import (
    generate_trip_schedule
)

schedule_bp = Blueprint(
    "schedule",
    __name__
)


# =====================================================
# Generate Dynamic Trip Schedule
# =====================================================

@schedule_bp.route(
    "/generate_schedule",
    methods=["POST"]
)
def generate_schedule():

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
        # Generate Schedule
        # =============================================

        result = generate_trip_schedule(
            data
        )

        # =============================================
        # Handle Service Failure
        # =============================================

        if not result.get(
            "success",
            False
        ):

            return jsonify(result), 500

        return jsonify(result)

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500