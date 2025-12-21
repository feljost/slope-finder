from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from slope_finder_backend.constants import ski_resorts
from slope_finder_backend.services.routing import calculate_air_distance
from slope_finder_backend.services.weather import get_weather_data
from slope_finder_backend.pipelines.get_resort_info import enrich_resorts_with_info
from slope_finder_backend.models import Location
from slope_finder_backend.models import SkiResortsResponse
from slope_finder_backend.models import WeatherRequest
from slope_finder_backend.models import WeatherData

app = FastAPI(title="Slope Finder Backend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/resorts-info")
def get_ski_resorts_by_distance(
    lat: float,
    lng: float,
    page: int = 1,
    page_size: int = 10,
    date: str | None = None,
) -> SkiResortsResponse:
    """
    Get ski resorts ordered by driving distance from the given location with pagination.

    Process:
    1. Sort all resorts by air distance
    2. Paginate - get resorts for the requested page
    3. Enrich resorts with driving distances, snow reports, and weather data
    4. Return paginated results

    Supports infinite scrolling by incrementing the page parameter.

    Args:
        lat: User's latitude
        lng: User's longitude
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
            lat,
            lng,
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
            "page": page,
            "page_size": page_size,
            "total_resorts": len(ski_resorts),
            "has_more": False,
            "resorts": [],
        }

    # Step 3: Enrich resorts with driving distances, snow reports, and weather
    resorts_with_metadata = enrich_resorts_with_info(lat, lng, page_resorts, date)

    return {
        "page": page,
        "page_size": page_size,
        "total_resorts": len(ski_resorts),
        "has_more": end_idx < len(ski_resorts),
        "resorts": resorts_with_metadata,
    }
