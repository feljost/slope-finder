from fastapi import FastAPI
from fastapi import HTTPException
from concurrent.futures import ThreadPoolExecutor, as_completed

from slope_finder_backend.constants import ski_resorts
from slope_finder_backend.services.routing import get_driving_distances_batch
from slope_finder_backend.services.routing import calculate_air_distance
from slope_finder_backend.services.snow_report import scrape_snow_reports_batch
from slope_finder_backend.services.weather import get_weather_data
from slope_finder_backend.models import Location
from slope_finder_backend.models import SkiResortsResponse
from slope_finder_backend.models import WeatherRequest
from slope_finder_backend.models import WeatherData

app = FastAPI(title="Slope Finder Backend")


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/ski-resorts/by-distance")
def get_ski_resorts_by_distance(
    location: Location,
    page: int = 1,
    page_size: int = 10,
    date: str | None = None,
) -> SkiResortsResponse:
    """
    Get ski resorts ordered by driving distance from the given location with pagination.

    Process:
    1. Sort all resorts by air distance
    2. Paginate - get resorts for the requested page
    3. Fetch driving distances and weather data in parallel (if date is provided)
    4. Fetch snow reports for the page
    5. Return resorts with distance, duration, snow reports, and weather

    Supports infinite scrolling by incrementing the page parameter.

    Args:
        location: User's location (lat, lng)
        page: Page number (default: 1)
        page_size: Number of resorts per page (max: 10)
        date: Optional date for weather data in YYYY-MM-DD format
    """
    if page < 1 or page_size > 10:
        return HTTPException(
            status_code=422, detail="page_size must be <= 10 and page must be >= 1"
        )

    # Step 1: Calculate air distance for all resorts and sort
    resorts_with_metadata = []
    for resort in ski_resorts:
        air_distance = calculate_air_distance(
            location.lat,
            location.lng,
            resort["location"]["lat"],
            resort["location"]["lng"],
        )
        resorts_with_metadata.append(
            {"resort": resort, "air_distance_km": air_distance}
        )

    # Sort by air distance
    resorts_with_metadata.sort(key=lambda x: x["air_distance_km"])

    # Step 2: Paginate - get the resorts for the requested page
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    page_resorts = resorts_with_metadata[start_idx:end_idx]

    # If no resorts on this page, return empty
    if not page_resorts:
        return {
            "location": location.dict(),
            "page": page,
            "page_size": page_size,
            "total_resorts": len(ski_resorts),
            "has_more": False,
            "resorts": [],
        }

    # Step 3: Get driving distances and weather data in parallel
    destinations = [
        {"lat": r["resort"]["location"]["lat"], "lng": r["resort"]["location"]["lng"]}
        for r in page_resorts
    ]

    def fetch_driving_distances():
        return get_driving_distances_batch(location.lat, location.lng, destinations)

    def fetch_weather_data():
        weather_data = {}
        if date:
            for item in page_resorts:
                resort_lat = item["resort"]["location"]["lat"]
                resort_lng = item["resort"]["location"]["lng"]
                try:
                    weather = get_weather_data(resort_lat, resort_lng, date)
                    weather_data[item["resort"]["name"]] = weather.dict()
                except Exception:
                    weather_data[item["resort"]["name"]] = None
        return weather_data

    # Execute driving distances and weather fetching in parallel
    with ThreadPoolExecutor(max_workers=2) as executor:
        driving_future = executor.submit(fetch_driving_distances)
        weather_future = executor.submit(fetch_weather_data)

        route_infos = driving_future.result()
        weather_data = weather_future.result()

    # Step 4: Get snow reports for this page
    snow_reports = scrape_snow_reports_batch(
        [r["resort"]["snowreport_url"] for r in page_resorts]
    )

    # Step 5: Build response with driving distances, snow reports & weather
    resorts_with_distance = []
    for i, item in enumerate(page_resorts):
        route_info = route_infos[i]
        if route_info:
            resort_data = {
                **item["resort"],
                "air_distance_km": round(item["air_distance_km"], 2),
                "distance_km": route_info["distance_km"],
                "duration_minutes": route_info["duration_minutes"],
                "snow_report": snow_reports[item["resort"]["snowreport_url"]][
                    "data"
                ],
            }
            # Add weather data if available
            if date and item["resort"]["name"] in weather_data:
                resort_data["weather"] = weather_data[item["resort"]["name"]]

            resorts_with_distance.append(resort_data)

    return {
        "page": page,
        "page_size": page_size,
        "total_resorts": len(ski_resorts),
        "has_more": end_idx < len(ski_resorts),
        "resorts": resorts_with_distance,
    }


@app.post("/weather")
def get_weather(request: WeatherRequest) -> WeatherData:
    """
    Get weather data for a specific location and date.

    Returns aggregated weather conditions for three periods:
    - Morning (8-10): Average temp, summed precipitation/snowfall, average cloud cover & visibility
    - Midday (11-13): Average temp, summed precipitation/snowfall, average cloud cover & visibility
    - Afternoon (14-17): Average temp, summed precipitation/snowfall, average cloud cover & visibility

    Also includes total snowfall from the previous 24 hours (entire previous day).

    Args:
        request: WeatherRequest with lat, lng, and date (YYYY-MM-DD format)

    Returns:
        WeatherData with morning, midday, and afternoon weather periods, plus 24h snowfall
    """
    try:
        return get_weather_data(request.lat, request.lng, request.date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weather data: {str(e)}")
