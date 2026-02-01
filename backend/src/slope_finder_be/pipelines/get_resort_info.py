import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from slope_finder_be.models import Location
from slope_finder_be.services.routing import get_routes_batch_google
from slope_finder_be.services.snow_report import scrape_snow_reports_batch
from slope_finder_be.services.weather import get_weather_data_batch


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
        start = time.time()
        # Use the date to create a departure time (8:00 AM on the target date)
        departure_time = date.replace(hour=8, minute=0, second=0, microsecond=0)
        result = get_routes_batch_google(lat, lng, destinations, departure_time)
        print(f"[PROFILE] fetch_driving_distances: {time.time() - start:.2f}s")
        return result

    def fetch_weather_data():
        start = time.time()
        locations = [
            {
                "name": item["resort"]["name"],
                "lat": item["resort"]["location"]["lat"],
                "lng": item["resort"]["location"]["lng"],
            }
            for item in page_resorts
        ]
        weather_results = get_weather_data_batch(locations, date)
        print(f"[PROFILE] fetch_weather_data: {time.time() - start:.2f}s")
        return {
            name: weather.dict() if weather else None
            for name, weather in weather_results.items()
        }

    def fetch_snow_reports():
        start = time.time()
        result = scrape_snow_reports_batch(
            [r["resort"]["snowreport_url"] for r in page_resorts]
        )
        print(f"[PROFILE] fetch_snow_reports: {time.time() - start:.2f}s")
        return result

    # Execute all data fetching in parallel
    overall_start = time.time()
    with ThreadPoolExecutor(max_workers=3) as executor:
        driving_future = executor.submit(fetch_driving_distances)
        weather_future = executor.submit(fetch_weather_data)
        snow_reports_future = executor.submit(fetch_snow_reports)

        route_infos = driving_future.result()
        weather_data = weather_future.result()
        snow_reports = snow_reports_future.result()
    print(f"[PROFILE] Total parallel fetch: {time.time() - overall_start:.2f}s")

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
            # Add weather data if available and not None
            weather = weather_data.get(item["resort"]["name"])
            if weather is not None:
                resort_data["weather"] = weather

            enriched_resorts.append(resort_data)

    return enriched_resorts
