import math


# =====================================================
# Haversine Distance (Meters)
# =====================================================

def haversine_m(
    lat1,
    lon1,
    lat2,
    lon2
):

    if (
        lat1 is None
        or lon1 is None
        or lat2 is None
        or lon2 is None
    ):

        return float("nan")

    R = 6371000.0

    phi1 = math.radians(lat1)

    phi2 = math.radians(lat2)

    dphi = math.radians(
        lat2 - lat1
    )

    dlambda = math.radians(
        lon2 - lon1
    )

    a = (
        math.sin(dphi / 2.0) ** 2
        +
        math.cos(phi1)
        *
        math.cos(phi2)
        *
        math.sin(dlambda / 2.0) ** 2
    )

    return (
        2
        * R
        * math.asin(
            math.sqrt(a)
        )
    )


# =====================================================
# Haversine Distance (Kilometers)
# =====================================================

def haversine_km(
    lat1,
    lon1,
    lat2,
    lon2
):

    return round(

        haversine_m(
            lat1,
            lon1,
            lat2,
            lon2
        ) / 1000.0,

        2
    )