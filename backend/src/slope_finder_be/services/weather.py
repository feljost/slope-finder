import os
import requests
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

from dotenv import load_dotenv
from slope_finder_be.models import WeatherData, WeatherPeriod

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_WEATHER_BASE_URL = "https://weather.googleapis.com/v1"


def get_weather_data(lat: float, lng: float, date: datetime) -> WeatherData:
    """Get weather data for a specific location and date from Google Weather API."""
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not set in environment variables")

    target_date = date.date()
    previous_date = target_date - timedelta(days=1)

    now = datetime.now()

    # IMPORTANT: The Google Weather API does not support querying by date range.
    # The hourly endpoints only accept a `hours` parameter that fetches N hours
    # from "now" (forward for forecast, backward for history). There is no way to
    # request "give me weather for Thursday" directly. So we must:
    # 1. Calculate how many hours from now until the data we need
    # 2. Request that many hours
    # 3. Filter the response to extract the specific hours we care about
    #
    # Calculate the time range we actually need:
    # - Previous day 00:00 (for 24h snowfall)
    # - Target day up to 17:00 (to cover afternoon period ending at 16:xx)
    start_needed = datetime.combine(previous_date, datetime.min.time())
    end_needed = datetime.combine(target_date, datetime.min.time().replace(hour=17))

    # Calculate how many hours of history and forecast we need
    history_hours = 0
    forecast_hours = 0

    if start_needed < now:
        # Some of the needed data is in the past (Google Weather API history limit is 24 hours)
        history_hours = min(int((now - start_needed).total_seconds() / 3600) + 1, 24)

    if end_needed > now:
        # Some of the needed data is in the future
        forecast_hours = min(int((end_needed - now).total_seconds() / 3600) + 1, 168)

    # weather data
    with ThreadPoolExecutor(max_workers=2) as executor:
        forecast_future = executor.submit(_fetch_google_weather, "forecast", lat, lng, forecast_hours) if forecast_hours > 0 else None
        history_future = executor.submit(_fetch_google_weather, "history", lat, lng, history_hours) if history_hours > 0 else None
        
        forecast = forecast_future.result() if forecast_future else []
        history = history_future.result() if history_future else []

    # Combine all hours for easier filtering
    all_hours = history + forecast

    # Group hours by time period for target date (using local time)
    morning, midday, afternoon = [], [], []
    snowfall_prev_day = 0.0

    for h in all_hours:
        display = h.get("displayDateTime", {})
        h_date = (display.get("year"), display.get("month"), display.get("day"))
        hour = display.get("hours", 0)

        # Collect hours for target date weather periods
        if h_date == (target_date.year, target_date.month, target_date.day):
            if 8 <= hour <= 10:
                morning.append(h)
            elif 11 <= hour <= 13:
                midday.append(h)
            elif 14 <= hour <= 16:
                afternoon.append(h)

        # Sum snowfall from previous day (24h before target date)
        if h_date == (previous_date.year, previous_date.month, previous_date.day):
            snowfall_prev_day += _get_snowfall_cm(h)

    return WeatherData(
        snowfall_prev_24h_cm=round(snowfall_prev_day, 1),
        morning=_create_period(morning, "morning"),
        midday=_create_period(midday, "midday"),
        afternoon=_create_period(afternoon, "afternoon"),
    )


def get_weather_data_batch(
    locations: list[dict], date: datetime
) -> dict[str, WeatherData | None]:
    """
    Get weather data for multiple locations in parallel.

    Args:
        locations: List of dicts with 'name', 'lat', 'lng' keys
        date: Target datetime for weather data

    Returns:
        Dict mapping location name to WeatherData (or None if fetch failed)
    """
    def fetch_single(location: dict) -> tuple[str, WeatherData | None]:
        name = location["name"]
        try:
            weather = get_weather_data(location["lat"], location["lng"], date)
            return (name, weather)
        except Exception:
            return (name, None)

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(fetch_single, locations))

    return dict(results)


def _fetch_google_weather(endpoint: str, lat: float, lng: float, hours: int) -> list[dict]:
    """Fetch data from Google Weather API with pagination. Endpoint is 'forecast' or 'history'."""
    url = f"{GOOGLE_WEATHER_BASE_URL}/{endpoint}/hours:lookup"
    hours_key = f"{endpoint}Hours"  # forecastHours or historyHours
    params = {"key": GOOGLE_API_KEY, "location.latitude": lat, "location.longitude": lng, "hours": hours}
    all_hours = []

    while len(all_hours) < hours:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        all_hours.extend(data.get(hours_key, []))
        if "nextPageToken" not in data:
            break
        params["pageToken"] = data["nextPageToken"]

    return all_hours


def _get_snowfall_cm(h: dict) -> float:
    """Extract snowfall in cm from hour data using snowQpf field."""
    precip = h.get("precipitation", {})
    snow_qpf_mm = precip.get("snowQpf", {}).get("quantity", 0)
    return snow_qpf_mm / 10  # Convert mm to cm


def _create_period(hours: list[dict], period_name: str) -> WeatherPeriod:
    """Create a WeatherPeriod by aggregating data across multiple hours."""
    if not hours:
        raise ValueError(f"No data available for {period_name}")

    temps = [h.get("temperature", {}).get("degrees") for h in hours]
    clouds = [h.get("cloudCover") for h in hours]
    vis = [h.get("visibility", {}).get("distance") for h in hours]
    precip = [h.get("precipitation", {}).get("qpf", {}).get("quantity", 0) for h in hours]

    temps = [t for t in temps if t is not None]
    clouds = [c for c in clouds if c is not None]
    vis = [v for v in vis if v is not None]

    return WeatherPeriod(
        time=hours[0].get("interval", {}).get("startTime", ""),
        temperature_celsius=round(sum(temps) / len(temps), 1) if temps else None,
        precipitation_mm=round(sum(precip), 1),
        snowfall_cm=round(sum(_get_snowfall_cm(h) for h in hours), 1),
        cloud_cover_percent=int(sum(clouds) / len(clouds)) if clouds else None,
        visibility_m=round(sum(vis) / len(vis) * 1000, 0) if vis else None,  # km to m
    )
