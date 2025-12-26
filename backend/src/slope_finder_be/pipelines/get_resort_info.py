from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from slope_finder_be.models import Location
from slope_finder_be.services.routing import get_routes_batch_google
from slope_finder_be.services.snow_report import scrape_snow_reports_batch
from slope_finder_be.services.weather import get_weather_data


def enrich_resorts_with_info(
    lat: float,
    lng: float,
    page_resorts: list[dict],
    date: datetime
) -> list[dict]:
    """
    Enrich resort data with driving/transit routes, snow reports, and weather information.

    This function performs the following operations:
    1. Fetches driving and transit routes, snow reports, and weather data in parallel
    2. Combines all data into enriched resort objects

    Args:
        lat: User's latitude
        lng: User's longitude
        page_resorts: List of resorts with metadata (resort data and air_distance_km)
        date: Datetime object for weather data and route departure time

    Returns:
        List of enriched resort dictionaries with driving/transit routes, snow reports, and weather.
        Each resort includes:
        - driving: {distance_km, duration_minutes} or None
        - transit: {distance_km, duration_minutes} or None
    """
    # Prepare destinations for routing
    destinations = [
        {"lat": r["resort"]["location"]["lat"], "lng": r["resort"]["location"]["lng"]}
        for r in page_resorts
    ]

    def fetch_driving_distances():
        # Use the date to create a departure time (8:00 AM on the target date)
        departure_time = date.replace(hour=8, minute=0, second=0, microsecond=0)
        return get_routes_batch_google(lat, lng, destinations, departure_time)

    def fetch_weather_data():
        weather_data = {}
        for item in page_resorts:
            resort_lat = item["resort"]["location"]["lat"]
            resort_lng = item["resort"]["location"]["lng"]
            try:
                weather = get_weather_data(resort_lat, resort_lng, date)
                weather_data[item["resort"]["name"]] = weather.dict()
            except Exception:
                weather_data[item["resort"]["name"]] = None
        return weather_data

    def fetch_snow_reports():
        return scrape_snow_reports_batch(
            [r["resort"]["snowreport_url"] for r in page_resorts]
        )

    # Execute all data fetching in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        driving_future = executor.submit(fetch_driving_distances)
        weather_future = executor.submit(fetch_weather_data)
        snow_reports_future = executor.submit(fetch_snow_reports)

        route_infos = driving_future.result()
        weather_data = weather_future.result()
        snow_reports = snow_reports_future.result()

    # Build enriched resort data
    enriched_resorts = []
    for i, item in enumerate(page_resorts):
        route_info = route_infos[i]
        if route_info:
            resort_data = {
                **item["resort"],
                "air_distance_km": round(item["air_distance_km"], 2),
                "distance_km": (
                    route_info["driving"]["distance_km"]
                    or route_info["transit"]["distance_km"]
                    or round(item["air_distance_km"], 2)
                    ),
                "duration_driving_minutes": route_info["driving"]["duration_minutes"],
                "duration_transit_minutes": route_info["transit"]["duration_minutes"],
                "maps_directions_url_driving": route_info["driving"]["maps_directions_url"],
                "maps_directions_url_transit": route_info["transit"]["maps_directions_url"],
                "snow_report": snow_reports[item["resort"]["snowreport_url"]]["data"],
            }
            # Add weather data if available
            if item["resort"]["name"] in weather_data:
                resort_data["weather"] = weather_data[item["resort"]["name"]]

            enriched_resorts.append(resort_data)

    return enriched_resorts
