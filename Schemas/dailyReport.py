# TABLE_NAME = "weatherdata.district_wise_7dayfc_severity"

# DESCRIPTION = """
# District-wise 7-day weather forecast.

# Contains:
# - Temperature
# - Rainfall
# - Humidity
# - Wind
# - Visibility
# - Weather Condition
# - Severity
# """

# COLUMNS = {
#     "days": "Forecast day",
#     "date": "Forecast date",
#     "district": "District name",
#     "indus_circle": "Circle code",
#     "temp_min": "Minimum temperature",
#     "temp_max": "Maximum temperature",
#     "rain_percent": "Rain probability",
#     "rain_precip": "Rainfall (mm)",
#     "wind": "Wind speed",
#     "visibility": "Visibility",
#     "humidity": "Humidity",
#     "condition_text": "Weather condition",
#     "temp_max_severity": "Temperature severity",
#     "rain_severity": "Rain severity"
# }

DAILY_SCHEMA = """
Table:
weatherdata.district_wise_7dayfc_severity

Columns

days
date
indus_circle
district
temp_min
temp_max
rain_percent
rain_precip
wind
visibility
humidity
condition_text
temp_max_severity
temp_min_severity
rain_severity
wind_severity
visibility_severity
humidity_severity
inserted_at
"""