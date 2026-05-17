import numpy as np

from app.utils.haversine import (
    haversine_m
)

from app.utils.constants import (

    HOTEL_CATEGORY,

    RESTAURANT_CATEGORY,

    DEFAULT_RADIUS_M,

    DEFAULT_PLACE_LIMIT
)

from app.utils.validators import (
    validate_coordinates
)

from app.services.geoapify_service import (

    geocode_location,

    extract_coordinates,

    fetch_nearby_places
)


# =====================================================
# Search Hotels
# =====================================================

def search_hotels_service(data):

    try:

        state = data.get(
            "state",
            ""
        ).strip()

        sightseeing = data.get(
            "sightseeing",
            ""
        ).strip()

        max_budget = float(

            data.get(
                "max_budget",
                5000
            )
        )

        # =============================================
        # Geocode Sightseeing Place
        # =============================================

        geo = geocode_location(
            f"{sightseeing}, {state}"
        )

        if not geo.get("success"):

            return {

                "success": False,

                "error":
                    "Location not found"
            }

        lat, lon = extract_coordinates(
            geo["data"]
        )

        if not validate_coordinates(
            lat,
            lon
        ):

            return {

                "success": False,

                "error":
                    "Invalid coordinates"
            }

        # =============================================
        # Search Nearby Hotels
        # =============================================

        hotel_data = fetch_nearby_places(

            lat=lat,

            lon=lon,

            categories=HOTEL_CATEGORY,

            radius_m=DEFAULT_RADIUS_M,

            limit=DEFAULT_PLACE_LIMIT
        )

        if not hotel_data.get("success"):

            return {

                "success": False,

                "error":
                    "Failed to fetch hotels"
            }

        hotel_features = hotel_data[
            "data"
        ].get(
            "features",
            []
        )

        hotels = []

        for feature in hotel_features:

            properties = feature.get(
                "properties",
                {}
            )

            hotel_name = properties.get(
                "name",
                "Unnamed Hotel"
            )

            # =========================================
            # Estimated Price
            # =========================================

            estimated_price = np.random.randint(
                1000,
                10000
            )

            # =========================================
            # Budget Filter
            # =========================================

            if estimated_price > max_budget:

                continue

            hotels.append({

                "name":
                    hotel_name,

                "rating":
                    round(
                        np.random.uniform(
                            3.5,
                            5.0
                        ),
                        1
                    ),

                "price":
                    estimated_price,

                "nearby":
                    sightseeing,

                "address":
                    properties.get(
                        "formatted",
                        ""
                    )
            })

        return {

            "success": True,

            "hotels": hotels
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }


# =====================================================
# Nearby Places
# =====================================================

def nearby_places_service(

    lat,
    lon,
    t_raw="restaurant",
    radius_m=DEFAULT_RADIUS_M
):

    try:

        # =============================================
        # Validate Coordinates
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

        type_tokens = [

            s.strip().lower()

            for s in str(t_raw).split(",")

            if s.strip()
        ]

        categories = []

        for tok in type_tokens:

            if tok in (

                "hotel",
                "hotels",
                "accommodation"
            ):

                categories.append(
                    HOTEL_CATEGORY
                )

            elif tok in (

                "restaurant",
                "restaurants",
                "food"
            ):

                categories.append(
                    RESTAURANT_CATEGORY
                )

        if not categories:

            categories = [
                RESTAURANT_CATEGORY
            ]

        merged = []

        seen = set()

        # =============================================
        # Geoapify Nearby Places
        # =============================================

        for cat in categories:

            result = fetch_nearby_places(

                lat=lat,

                lon=lon,

                categories=cat,

                radius_m=radius_m,

                limit=DEFAULT_PLACE_LIMIT
            )

            if not result.get("success"):

                continue

            data = result["data"]

            for f in data.get(
                "features",
                []
            ):

                p = f.get(
                    "properties",
                    {}
                )

                g = f.get(
                    "geometry",
                    {}
                ).get(
                    "coordinates",
                    [None, None]
                )

                pid = (

                    p.get("place_id")

                    or p.get("xid")

                    or p.get("osm_id")

                    or (
                        p.get("name"),
                        g[0],
                        g[1]
                    )
                )

                if pid in seen:

                    continue

                seen.add(pid)

                poi_lat = g[1]

                poi_lon = g[0]

                dist_m = haversine_m(

                    lat,
                    lon,

                    poi_lat,
                    poi_lon

                ) if (
                    poi_lat
                    and poi_lon
                ) else None

                merged.append({

                    "name":
                        p.get(
                            "name",
                            "Unnamed"
                        ),

                    "address":
                        p.get(
                            "formatted",
                            ""
                        ),

                    "coords": {

                        "lat":
                            poi_lat,

                        "lon":
                            poi_lon
                    },

                    "distance_m":
                        int(dist_m)
                        if dist_m is not None
                        else None,

                    "distance_km":
                        round(
                            dist_m / 1000.0,
                            2
                        )
                        if dist_m is not None
                        else None,

                    "category":
                        p.get("categories")

                        or p.get("kinds")

                        or cat,

                    "rating":
                        p.get("rating")

                        or p.get("rate"),

                    "popularity":
                        (
                            p.get("rank")
                            or {}
                        ).get("popularity")
                        if isinstance(
                            p.get("rank"),
                            dict
                        )
                        else p.get(
                            "popularity"
                        ),

                    "website":
                        p.get("website"),

                    "phone":
                        p.get("phone"),

                    "opening_hours":
                        p.get(
                            "opening_hours"
                        )
                })

        # =============================================
        # Sort Places
        # =============================================

        merged.sort(

            key=lambda x: (

                (
                    x.get(
                        "distance_m"
                    ) is None
                ),

                x.get(
                    "distance_m",
                    10**9
                ),

                -(
                    x.get(
                        "popularity"
                    ) or 0
                )
            )
        )

        return {

            "success": True,

            "places": merged
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }