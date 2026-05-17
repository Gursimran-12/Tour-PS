import hashlib
import time
import requests

from flask import current_app

from app.utils.constants import (

    CACHE_TTL_SECONDS,

    DEFAULT_TIMEOUT
)

from app.utils.validators import (
    is_empty
)

from app.services.sentiment_service import (
    sentiment_for_text,
    extract_text
)


# =====================================================
# Reviews Cache
# =====================================================

REVIEWS_CACHE = {}


# =====================================================
# Fetch Google Reviews
# =====================================================

def fetch_place_reviews(
    name,
    address="",
    lat=None,
    lon=None
):

    # =============================================
    # Validation
    # =============================================

    if is_empty(name):

        return {

            "success": False,

            "error":
                "Missing place name"
        }

    # =============================================
    # Generate Cache Key
    # =============================================

    cache_key = hashlib.sha256(

        f"{name}|{address}".encode()

    ).hexdigest()

    cached = REVIEWS_CACHE.get(
        cache_key
    )

    # =============================================
    # Return Cached Result
    # =============================================

    if cached and (

        time.time()
        - cached.get("ts", 0)

        < CACHE_TTL_SECONDS
    ):

        return cached["data"]

    # =============================================
    # Search Place Using SerpAPI
    # =============================================

    try:

        search_response = requests.get(

            current_app.config[
                "SERPAPI_BASE_URL"
            ],

            params={

                "engine":
                    "google_maps",

                "q":
                    f"{name} {address}",

                "hl":
                    "en",

                "api_key":
                    current_app.config[
                        "SERPAPI_API_KEY"
                    ]
            },

            timeout=DEFAULT_TIMEOUT
        )

    except Exception as e:

        return {

            "success": False,

            "error":
                "SerpAPI search failed",

            "details":
                str(e)
        }

    # =============================================
    # Validate Search Response
    # =============================================

    if search_response.status_code != 200:

        return {

            "success": False,

            "error":
                "SerpAPI search error",

            "preview":
                search_response.text
        }

    search_json = search_response.json()

    place_results = search_json.get(
        "place_results",
        {}
    )

    data_id = place_results.get(
        "data_id"
    )

    if not data_id:

        return {

            "success": False,

            "error":
                "No data_id found",

            "preview":
                search_json
        }

    # =============================================
    # Fetch Reviews
    # =============================================

    try:

        review_response = requests.get(

            current_app.config[
                "SERPAPI_BASE_URL"
            ],

            params={

                "engine":
                    "google_maps_reviews",

                "data_id":
                    data_id,

                "hl":
                    "en",

                "api_key":
                    current_app.config[
                        "SERPAPI_API_KEY"
                    ]
            },

            timeout=DEFAULT_TIMEOUT
        )

    except Exception as e:

        return {

            "success": False,

            "error":
                "Reviews request failed",

            "details":
                str(e)
        }

    # =============================================
    # Validate Review Response
    # =============================================

    if review_response.status_code != 200:

        return {

            "success": False,

            "error":
                "Review fetch failed",

            "preview":
                review_response.text
        }

    review_json = review_response.json()

    # =============================================
    # Process Reviews
    # =============================================

    reviews_output = []

    total = 0

    positive = 0

    neutral = 0

    negative = 0

    compound_sum = 0.0

    for review in review_json.get(
        "reviews",
        []
    ):

        text = extract_text(
            review
        )

        sentiment = sentiment_for_text(
            text
        )

        total += 1

        compound_sum += sentiment.get(
            "compound",
            0.0
        )

        if sentiment.get(
            "label"
        ) == "positive":

            positive += 1

        elif sentiment.get(
            "label"
        ) == "negative":

            negative += 1

        else:

            neutral += 1

        user = review.get(
            "user",
            {}
        ) or {}

        reviews_output.append({

            "author":
                user.get(
                    "name",
                    "Anonymous"
                ),

            "rating":
                review.get(
                    "rating"
                ),

            "date":
                review.get(
                    "date"
                ),

            "text":
                text,

            "sentiment":
                sentiment
        })

    # =============================================
    # Sentiment Summary
    # =============================================

    summary = {

        "count":
            total,

        "positive":
            positive,

        "neutral":
            neutral,

        "negative":
            negative,

        "avg_compound":
            round(
                compound_sum / total,
                3
            ) if total else 0.0
    }

    # =============================================
    # Final Output
    # =============================================

    result = {

        "success": True,

        "place_info":
            review_json.get(
                "place_info",
                {}
            ),

        "reviews":
            reviews_output,

        "sentiment_summary":
            summary
    }

    # =============================================
    # Cache Result
    # =============================================

    REVIEWS_CACHE[cache_key] = {

        "ts":
            time.time(),

        "data":
            result
    }

    return result