import requests
import traceback

from flask import current_app

from app.utils.constants import (

    DEFAULT_TIMEOUT,

    ROUTING_TIMEOUT,

    DEFAULT_PLACE_LIMIT,

    DEFAULT_RADIUS_M
)

from app.utils.validators import (

    validate_coordinates,

    is_empty
)


# =====================================================
# Geocode Location
# =====================================================

def geocode_location(
    text,
    limit=1
):

    try:

        # =============================================
        # Validation
        # =============================================

        if is_empty(text):

            return {

                "success": False,

                "error":
                    "Location text is required"
            }

        # =============================================
        # Force India Bias
        # =============================================

        if "india" not in text.lower():

            text = f"{text}, India"

        url = (
            "https://api.geoapify.com/"
            "v1/geocode/search"
        )

        params = {

            "text":
                text,

            "limit":
                limit,

            # =============================================
            # Deployment Safe Bias
            # =============================================

            "filter":
                "countrycode:in",


            "format":
                "json",

            "apiKey":
                current_app.config[
                    "GEOAPIFY_KEY"
                ]
        }

        response = requests.get(

            url,

            params=params,

            timeout=DEFAULT_TIMEOUT
        )
        print(response.url)
        print("\n========== GEOCODE STATUS ==========")
        print(response.status_code)

        response.raise_for_status()

        data = response.json()

        print("\n========== GEOCODE RESPONSE ==========")
        print(data)

        # =============================================
        # Empty Results Check
        # =============================================

        features = data.get(
            "features",
            []
        )

        if not features:

            return {

                "success": False,

                "error":
                    "No matching location found"
            }

        return {

            "success": True,

            "data": data
        }

    except Exception as e:

        print("\n========== GEOCODE ERROR ==========")

        print(traceback.format_exc())

        return {

            "success": False,

            "error": str(e)
        }


# =====================================================
# Reverse Geocode
# =====================================================

def reverse_geocode_service(
    lat,
    lon
):

    try:

        # =============================================
        # Validation
        # =============================================

        if not validate_coordinates(
            lat,
            lon
        ):

            return {

                "success": False,

                "error":
                    "Invalid coordinates"
            }

        url = (
            "https://api.geoapify.com/"
            "v1/geocode/reverse"
        )

        params = {

            "lat":
                lat,

            "lon":
                lon,

            "apiKey":
                current_app.config[
                    "GEOAPIFY_KEY"
                ]
        }

        response = requests.get(

            url,

            params=params,

            timeout=DEFAULT_TIMEOUT
        )

        print("\n========== REVERSE GEOCODE STATUS ==========")
        print(response.status_code)

        response.raise_for_status()

        data = response.json()

        print("\n========== REVERSE GEOCODE RESPONSE ==========")
        print(data)

        # =============================================
        # Extract Formatted Address
        # =============================================

        features = data.get(
            "features",
            []
        )

        formatted = "Unknown Location"

        if features:

            formatted = features[0].get(
                "properties",
                {}
            ).get(
                "formatted",
                "Unknown Location"
            )

        return {

            "success": True,

            "data": data,

            "formatted":
                formatted
        }

    except Exception as e:

        print("\n========== REVERSE GEOCODE ERROR ==========")

        print(traceback.format_exc())

        return {

            "success": False,

            "error": str(e)
        }


# =====================================================
# Autocomplete Suggestions
# =====================================================

def autocomplete_places(
    text,
    limit=10
):

    try:

        # =============================================
        # Validation
        # =============================================

        if is_empty(text):

            return {

                "success": False,

                "error":
                    "Search text is required"
            }

        url = (
            "https://api.geoapify.com/"
            "v1/geocode/autocomplete"
        )

        params = {

            "text":
                text,

            "limit":
                limit,

            # =============================================
            # India Bias
            # =============================================

            "filter":
                "countrycode:in",

            "apiKey":
                current_app.config[
                    "GEOAPIFY_KEY"
                ]
        }

        response = requests.get(

            url,

            params=params,

            timeout=DEFAULT_TIMEOUT
        )

        print("\n========== AUTOCOMPLETE STATUS ==========")
        print(response.status_code)

        response.raise_for_status()

        data = response.json()

        print("\n========== AUTOCOMPLETE RESPONSE ==========")
        print(data)

        suggestions = []

        for feature in data.get(
            "features",
            []
        ):

            props = feature.get(
                "properties",
                {}
            )

            suggestions.append({

                "formatted":
                    props.get(
                        "formatted"
                    ),

                "lat":
                    props.get(
                        "lat"
                    ),

                "lon":
                    props.get(
                        "lon"
                    )
            })

        return {

            "success": True,

            "results": suggestions
        }

    except Exception as e:

        print("\n========== AUTOCOMPLETE ERROR ==========")

        print(traceback.format_exc())

        return {

            "success": False,

            "error": str(e)
        }


# =====================================================
# Fetch Nearby Places
# =====================================================

def fetch_nearby_places(
    lat,
    lon,
    categories,
    radius_m=DEFAULT_RADIUS_M,
    limit=DEFAULT_PLACE_LIMIT
):

    try:

        # =============================================
        # Validation
        # =============================================

        if not validate_coordinates(
            lat,
            lon
        ):

            return {

                "success": False,

                "error":
                    "Invalid coordinates"
            }

        if is_empty(categories):

            return {

                "success": False,

                "error":
                    "Categories are required"
            }

        url = (
            "https://api.geoapify.com/"
            "v2/places"
        )

        params = {

            "categories":
                categories,

            "filter":
                f"circle:{lon},{lat},{radius_m}",

            "bias":
                f"proximity:{lon},{lat}",

            "limit":
                limit,

            "apiKey":
                current_app.config[
                    "GEOAPIFY_KEY"
                ]
        }

        response = requests.get(

            url,

            params=params,

            timeout=DEFAULT_TIMEOUT
        )

        print("\n========== PLACES STATUS ==========")
        print(response.status_code)

        response.raise_for_status()

        data = response.json()

        print("\n========== PLACES RESPONSE ==========")
        print(data)

        return {

            "success": True,

            "data": data
        }

    except Exception as e:

        print("\n========== PLACES ERROR ==========")

        print(traceback.format_exc())

        return {

            "success": False,

            "error": str(e)
        }


# =====================================================
# Routing Service
# =====================================================

def get_route_between_points(

    start_lat,
    start_lon,

    destination_lat,
    destination_lon,

    mode="drive"
):

    try:

        # =============================================
        # Validation
        # =============================================

        if not validate_coordinates(
            start_lat,
            start_lon
        ):

            return {

                "success": False,

                "error":
                    "Invalid start coordinates"
            }

        if not validate_coordinates(
            destination_lat,
            destination_lon
        ):

            return {

                "success": False,

                "error":
                    "Invalid destination coordinates"
            }

        # =============================================
        # Safe Mode Mapping
        # =============================================

        mode_mapping = {

            "drive":
                "drive",

            "car":
                "drive",

            "bicycle":
                "bicycle",

            "bike":
                "bicycle",

            "walk":
                "walk"
        }

        safe_mode = mode_mapping.get(
            mode,
            "drive"
        )

        url = (
            "https://api.geoapify.com/"
            "v1/routing"
        )

        params = {

            "waypoints":
                (
                    f"{start_lat},"
                    f"{start_lon}|"
                    f"{destination_lat},"
                    f"{destination_lon}"
                ),

            "mode":
                safe_mode,

            "details":
                "instruction_details",

            # =============================================
            # Better Route Optimization
            # =============================================

            "traffic":
                "approximated",

            "units":
                "metric",

            "apiKey":
                current_app.config[
                    "GEOAPIFY_KEY"
                ]
        }

        response = requests.get(

            url,

            params=params,

            timeout=ROUTING_TIMEOUT
        )

        print("\n========== ROUTING STATUS ==========")
        print(response.status_code)

        response.raise_for_status()

        data = response.json()

        print("\n========== ROUTING RESPONSE ==========")
        print(data)

        # =============================================
        # Empty Route Validation
        # =============================================

        features = data.get(
            "features",
            []
        )

        if not features:

            return {

                "success": False,

                "error":
                    "No route found"
            }

        return {

            "success": True,

            "data": data
        }

    except Exception as e:

        print("\n========== ROUTING ERROR ==========")

        print(traceback.format_exc())

        return {

            "success": False,

            "error": str(e)
        }


# =====================================================
# Extract Coordinates
# =====================================================

def extract_coordinates(
    geoapify_response
):

    try:

        features = geoapify_response.get(
            "features",
            []
        )

        if not features:

            return None, None

        props = features[0].get(
            "properties",
            {}
        )

        return (

            props.get("lat"),

            props.get("lon")
        )

    except Exception:

        return None, None


# =====================================================
# Normalize Geoapify Places
# =====================================================

def normalize_places(
    features
):

    places = []

    for feature in features:

        props = feature.get(
            "properties",
            {}
        )

        geometry = feature.get(
            "geometry",
            {}
        )

        coords = geometry.get(
            "coordinates",
            [None, None]
        )

        lon = coords[0]

        lat = coords[1]

        places.append({

            "name":
                props.get(
                    "name",
                    "Unnamed Place"
                ),

            "lat":
                lat,

            "lon":
                lon,

            "address":
                props.get(
                    "formatted",
                    ""
                ),

            "categories":
                ", ".join(

                    props.get(
                        "categories",
                        []
                    )
                ),

            "place_id":
                props.get(
                    "place_id"
                ),

            "website":
                props.get(
                    "website"
                ),

            "phone":
                props.get(
                    "phone"
                ),

            "rating":
                props.get(
                    "rating"
                ),

            "city":
                props.get(
                    "city"
                ),

            "state":
                props.get(
                    "state"
                )
        })

    return places