# =====================================================
# Validate Coordinates
# =====================================================

def validate_coordinates(
    lat,
    lon
):

    if lat is None or lon is None:

        return False

    try:

        lat = float(lat)

        lon = float(lon)

    except Exception:

        return False

    if lat < -90 or lat > 90:

        return False

    if lon < -180 or lon > 180:

        return False

    return True


# =====================================================
# Validate Empty String
# =====================================================

def is_empty(value):

    return (
        value is None
        or str(value).strip() == ""
    )


# =====================================================
# Validate Budget
# =====================================================

def validate_budget(budget):

    try:

        budget = float(budget)

        return budget > 0

    except Exception:

        return False


# =====================================================
# Validate Days
# =====================================================

def validate_days(days):

    try:

        days = int(days)

        return days > 0

    except Exception:

        return False