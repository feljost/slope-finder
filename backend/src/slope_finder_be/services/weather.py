import requests
from datetime import datetime
from datetime import timedelta

from slope_finder_be.models import WeatherData, WeatherPeriod, Location


def get_weather_data(lat: float, lng: float, date: datetime) -> WeatherData:
    """
    Get weather data for a specific location and date from Open-Meteo API.

    Args:
        lat: Latitude of the location
        lng: Longitude of the location
        date: Datetime object for the target date

    Returns:
        WeatherData object with morning, midday, and afternoon weather periods,
        plus total snowfall from the previous 24 hours
    """
    url = "https://api.open-meteo.com/v1/forecast"

    # Calculate previous day to get 24h snowfall data
    target_date = date.date()
    previous_day = target_date - timedelta(days=1)

    params = {
        "latitude": lat,
        "longitude": lng,
        "start_date": previous_day.isoformat(),
        "end_date": target_date.isoformat(),
        "hourly": [
            "temperature_2m",
            "precipitation",
            "snowfall",
            "cloud_cover",
            "visibility"
        ],
        "timezone": "auto"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temperatures = hourly.get("temperature_2m", [])
    precipitation = hourly.get("precipitation", [])
    snowfall = hourly.get("snowfall", [])
    cloud_cover = hourly.get("cloud_cover", [])
    visibility = hourly.get("visibility", [])

    # Collect indices for time ranges
    # Morning: 8-10, Midday: 11-13, Afternoon: 14-17
    morning_indices = []
    midday_indices = []
    afternoon_indices = []
    previous_day_indices = []

    for i, time_str in enumerate(times):
        time_obj = datetime.fromisoformat(time_str)
        hour = time_obj.hour

        # Collect indices for the previous day (for 24h snowfall calculation)
        if time_obj.date() == previous_day:
            previous_day_indices.append(i)

        # Only collect period indices for the target date
        if time_obj.date() == target_date:
            if 8 <= hour <= 10:
                morning_indices.append(i)
            elif 11 <= hour <= 13:
                midday_indices.append(i)
            elif 14 <= hour <= 16:
                afternoon_indices.append(i)

    def create_period(indices: list[int], period_name: str) -> WeatherPeriod:
        """Helper to create a WeatherPeriod by aggregating data across multiple hours."""
        if not indices:
            raise ValueError(f"No data available for {period_name}")

        # Calculate averages for temperature, cloud_cover, and visibility
        avg_temp = sum(temperatures[i] for i in indices) / len(indices)
        avg_cloud = sum(cloud_cover[i] for i in indices) / len(indices)
        avg_visibility = sum(visibility[i] for i in indices) / len(indices)

        # Calculate sums for precipitation and snowfall
        total_precip = sum(precipitation[i] for i in indices)
        total_snow = sum(snowfall[i] for i in indices)

        # Use the first time in the range as the period time
        return WeatherPeriod(
            time=times[indices[0]],
            temperature_celsius=round(avg_temp, 1),
            precipitation_mm=round(total_precip, 1),
            snowfall_cm=round(total_snow, 1),
            cloud_cover_percent=int(avg_cloud),
            visibility_m=round(avg_visibility, 0)
        )

    # Calculate 24h snowfall from the previous day
    snowfall_24h = sum(snowfall[i] for i in previous_day_indices) if previous_day_indices else 0.0

    return WeatherData(
        snowfall_prev_24h_cm=round(snowfall_24h, 1),
        morning=create_period(morning_indices, "morning (8-10)"),
        midday=create_period(midday_indices, "midday (11-13)"),
        afternoon=create_period(afternoon_indices, "afternoon (14-17)"),
    )
