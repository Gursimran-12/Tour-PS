import numpy as np

from app.utils.haversine import (
    haversine_m
)

from app.utils.helpers import (
    hhmm_to_minutes,
    minutes_to_hhmm
)

from app.utils.constants import (

    DEFAULT_RADIUS_M,

    DEFAULT_VISIT_MINUTES,

    DEFAULT_TRAVEL_BUFFER_MINUTES
)

from app.services.geoapify_service import (
    fetch_nearby_places
)


# =====================================================
# Constants
# =====================================================

DEFAULT_MAX_POIS = 6


# =====================================================
# Geoapify Category Mapping
# =====================================================

CATEGORY_MAPPING = {

    "religious":
        "religion.place_of_worship",

    "historical":
        "heritage",

    "educational":
        "education",

    "leisure":
        "entertainment",

    "adventure":
        "sport",

    "cultural":
        "tourism.sights",

    "shopping":
        "commercial.shopping_mall"
}


# =====================================================
# Normalize Places
# =====================================================

def normalize_places(
    features,
    user_lat,
    user_lon
):

    places = []

    for f in features:

        props = f.get(
            "properties",
            {}
        )

        geometry = f.get(
            "geometry",
            {}
        )

        coords = geometry.get(
            "coordinates",
            [None, None]
        )

        lon = coords[0]

        lat = coords[1]

        # =============================================
        # Validation
        # =============================================

        if lat is None or lon is None:

            continue

        place_name = props.get(
            "name",
            "Unnamed Place"
        )

        # =============================================
        # Skip Invalid Places
        # =============================================

        if (
            not place_name
            or place_name.strip() == ""
            or place_name.lower() == "unnamed place"
            or "unnamed" in place_name.lower()
            or len(place_name.strip()) < 3
        ):

            continue

        # =============================================
        # Distance Calculation
        # =============================================

        distance_km = round(

            haversine_m(

                user_lat,
                user_lon,

                lat,
                lon

            ) / 1000,

            1
        )

        # =============================================
        # Transport Suggestion
        # =============================================

        if distance_km <= 2:

            transport = "Walk"

        elif distance_km <= 8:

            transport = "Bike"

        else:

            transport = "Drive"

        # =============================================
        # Category Formatting
        # =============================================

        categories = props.get(
            "categories",
            []
        )

        category_text = ", ".join(
            categories[:2]
        )

        # =============================================
        # Place Object
        # =============================================

        places.append({

            "name":
                place_name,

            "lat":
                lat,

            "lon":
                lon,

            "address":
                props.get(
                    "formatted",
                    "Address unavailable"
                ),

            "categories":
                categories,

            "rating":
                round(
                    np.random.uniform(
                        3.8,
                        5.0
                    ),
                    1
                ),

            "visit_minutes":
                DEFAULT_VISIT_MINUTES,

            "description":
                props.get(
                    "formatted",
                    "Popular sightseeing attraction"
                ),

            "distance_km":
                distance_km,

            "transport":
                transport,

            "category_text":
                category_text
        })

    # =============================================
    # Sort By Distance
    # =============================================

    places = sorted(

        places,

        key=lambda x: x["distance_km"]
    )

    return places


# =====================================================
# Distance Matrix
# =====================================================

def compute_distance_matrix(
    places
):

    n = len(places)

    matrix = [

        [0 for _ in range(n)]

        for _ in range(n)
    ]

    for i in range(n):

        for j in range(n):

            if i == j:

                continue

            d = haversine_m(

                places[i]["lat"],
                places[i]["lon"],

                places[j]["lat"],
                places[j]["lon"]
            )

            matrix[i][j] = d

    return matrix


# =====================================================
# Greedy Schedule Builder
# =====================================================

def build_schedule(
    places,
    start_time,
    stop_time
):

    if not places:

        return []

    current_minutes = hhmm_to_minutes(
        start_time
    )

    end_minutes = hhmm_to_minutes(
        stop_time
    )

    itinerary = []

    for idx, p in enumerate(places):

        visit_duration = p.get(
            "visit_minutes",
            DEFAULT_VISIT_MINUTES
        )

        # =============================================
        # Stop If Time Ends
        # =============================================

        if (
            current_minutes
            + visit_duration
            > end_minutes
        ):

            break

        arrival_min = current_minutes

        current_minutes += visit_duration

        depart_min = current_minutes

        itinerary.append({

            "name":
                p["name"],

            "arrival_min":
                arrival_min,

            "depart_min":
                depart_min,

            "address":
                p["address"],

            "lat":
                p["lat"],

            "lon":
                p["lon"],

            "pred_score":
                p["rating"],

            "pred_minutes":
                visit_duration,

            "distance_km":
                p["distance_km"],

            "category":
                p["category_text"],

            "description":
                p["description"],

            "how_to_reach":
                p["transport"],

            "is_restaurant":
                False
        })

        # =============================================
        # Travel Buffer
        # =============================================

        current_minutes += (
            DEFAULT_TRAVEL_BUFFER_MINUTES
        )

    return itinerary


# =====================================================
# Main Schedule Generator
# =====================================================

def generate_trip_schedule(
    data
):

    lat = data.get(
        "lat"
    )

    lon = data.get(
        "lon"
    )

    # =============================================
    # Frontend Selected Domains
    # =============================================

    categories = data.get(
        "selected_domains",
        []
    )

    days = int(
        data.get(
            "stay_days",
            1
        )
    )

    start_time = data.get(
        "start_time",
        "09:00"
    )

    stop_time = data.get(
        "end_time",
        "18:00"
    )

    radius_m = int(
        data.get(
            "radius_m",
            DEFAULT_RADIUS_M
        )
    )

    max_pois = int(
        data.get(
            "max_pois_per_day",
            DEFAULT_MAX_POIS
        )
    )

    # =============================================
    # Convert Frontend Categories
    # To Geoapify Categories
    # =============================================

    geo_categories = []

    for c in categories:

        mapped = CATEGORY_MAPPING.get(
            c
        )

        if mapped:

            geo_categories.append(
                mapped
            )

    # =============================================
    # Fallback
    # =============================================

    if not geo_categories:

        geo_categories = [
            "tourism.sights"
        ]

    # =============================================
    # Fetch Nearby Places
    # =============================================

    places_data = fetch_nearby_places(

        lat=lat,

        lon=lon,

        categories=",".join(
            geo_categories
        ),

        radius_m=radius_m,

        limit=80
    )

    # =============================================
    # Handle Failure
    # =============================================

    if not places_data.get(
        "success"
    ):

        return {

            "success": False,

            "error":
                "Failed to fetch places"
        }

    features = places_data[
        "data"
    ].get(
        "features",
        []
    )

    # =============================================
    # No Features
    # =============================================

    if not features:

        return {

            "success": False,

            "error":
                "No famous places found"
        }

    # =============================================
    # Normalize Places
    # =============================================

    places = normalize_places(

        features,

        lat,

        lon
    )

    # =============================================
    # Shuffle Places
    # =============================================

    np.random.shuffle(
        places
    )

    # =============================================
    # Generate Day-wise Schedule
    # =============================================

    final_schedule = {}

    start_idx = 0

    for day in range(days):

        end_idx = (
            start_idx
            + max_pois
        )

        day_places = places[
            start_idx:end_idx
        ]

        # =============================================
        # Fallback If Empty
        # =============================================

        if not day_places:

            day_places = places[
                :max_pois
            ]

        itinerary = build_schedule(

            day_places,

            start_time,

            stop_time
        )

        final_schedule[
            f"day_{day + 1}"
        ] = itinerary

        start_idx += max_pois

    # =============================================
    # Final Response
    # =============================================

    return {

        "success": True,

        "schedule":
            final_schedule,

        "meta": {

            "total_days":
                days,

            "categories":
                categories,

            "geo_categories":
                geo_categories,

            "radius_km":
                round(
                    radius_m / 1000,
                    1
                ),

            "total_places":
                len(places)
        }
    }