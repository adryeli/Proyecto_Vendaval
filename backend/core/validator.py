REQUIRED_FIELDS = [
    "timestamp",
    "zone",
    "city",
    "temperature_c",
    "humidity_pct",
    "wind_kph",
    "rain_mm",
    "source"
]


def validate_record(record: dict) -> tuple:
    """
    Validate full weather record.

    Returns:
        (bool, str): (is_valid, message)
    """

    is_valid, msg = validate_required_fields(record)
    if not is_valid:
        return False, msg

    is_valid, msg = validate_types(record)
    if not is_valid:
        return False, msg

    is_valid, msg = validate_ranges(record)
    if not is_valid:
        return False, msg

    return True, "Record is valid"


# -----------------------------------
# 1. REQUIRED FIELDS
# -----------------------------------

def validate_required_fields(record: dict) -> tuple:
    for field in REQUIRED_FIELDS:
        if field not in record:
            return False, f"Missing field: {field}"
    return True, "OK"


# -----------------------------------
# 2. TYPES
# -----------------------------------

def validate_types(record: dict) -> tuple:

    if not isinstance(record["city"], str):
        return False, "city must be string"

    if not isinstance(record["zone"], str):
        return False, "zone must be string"

    if not isinstance(record["temperature_c"], (int, float)):
        return False, "temperature_c must be number"

    if not isinstance(record["humidity_pct"], (int, float)):
        return False, "humidity_pct must be number"

    if not isinstance(record["wind_kph"], (int, float)):
        return False, "wind_kph must be number"

    if not isinstance(record["rain_mm"], (int, float)):
        return False, "rain_mm must be number"

    return True, "OK"


# -----------------------------------
# 3. RANGES
# -----------------------------------

def validate_ranges(record: dict) -> tuple:

    temp = record["temperature_c"]
    humidity = record["humidity_pct"]
    wind = record["wind_kph"]
    rain = record["rain_mm"]

    # temperatura realista
    if temp < -20 or temp > 50:
        return False, "temperature out of range"

    # humedad %
    if humidity < 0 or humidity > 100:
        return False, "humidity must be between 0 and 100"

    # viento
    if wind < 0:
        return False, "wind cannot be negative"

    # lluvia
    if rain < 0:
        return False, "rain cannot be negative"

    return True, "OK"