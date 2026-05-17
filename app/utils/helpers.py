from datetime import datetime


# =====================================================
# Convert HH:MM to Minutes
# =====================================================

def hhmm_to_minutes(hhmm):

    h, m = hhmm.split(":")

    return int(h) * 60 + int(m)


# =====================================================
# Convert Minutes to HH:MM
# =====================================================

def minutes_to_hhmm(minutes):

    h = minutes // 60

    m = minutes % 60

    return f"{h:02d}:{m:02d}"


# =====================================================
# Safe Float Converter
# =====================================================

def safe_float(
    value,
    default=0.0
):

    try:

        return float(value)

    except Exception:

        return default


# =====================================================
# Safe Integer Converter
# =====================================================

def safe_int(
    value,
    default=0
):

    try:

        return int(value)

    except Exception:

        return default


# =====================================================
# Current Timestamp
# =====================================================

def current_timestamp():

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# =====================================================
# Remove Duplicate Dictionaries
# =====================================================

def unique_by_key(
    items,
    key
):

    seen = set()

    result = []

    for item in items:

        value = item.get(key)

        if value in seen:

            continue

        seen.add(value)

        result.append(item)

    return result