from fastapi import FastAPI
from fastapi import HTTPException

from slope_check_backend.constants import ski_resorts
from slope_check_backend.models import LocationQuery
from slope_check_backend.routing import get_driving_distances_batch
from slope_check_backend.utils import calculate_air_distance

app = FastAPI(title="Slope Check Backend")


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/ski-resorts/by-distance")
def get_ski_resorts_by_distance(
    location: LocationQuery,
    page: int = 1,
    page_size: int = 10,
):
    """
    Get ski resorts ordered by driving distance from the given location with pagination.

    Process:
    1. Sort all resorts by air distance
    2. Fetch driving distances for the requested page
    3. Return resorts with driving distance and duration

    Supports infinite scrolling by incrementing the page parameter.
    """
    if page < 1 or page_size > 10:
        return HTTPException(
            status_code=422,
            detail="page_size must be <= 10 and page must be >= 1"
            )

    # Step 1: Calculate air distance for all resorts and sort
    resorts_with_air_distance = []
    for resort in ski_resorts:
        air_distance = calculate_air_distance(
            location.lat,
            location.lng,
            resort["location"]["lat"],
            resort["location"]["lng"],
        )
        resorts_with_air_distance.append(
            {"resort": resort, "air_distance_km": air_distance}
        )

    # Sort by air distance
    resorts_with_air_distance.sort(key=lambda x: x["air_distance_km"])

    # Step 2: Paginate - get the resorts for the requested page
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    page_resorts = resorts_with_air_distance[start_idx:end_idx]

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

    # Step 3: Get driving distances for this page
    destinations = [
        {"lat": r["resort"]["location"]["lat"], "lng": r["resort"]["location"]["lng"]}
        for r in page_resorts
    ]
    route_infos = get_driving_distances_batch(location.lat, location.lng, destinations)

    # Step 4: Build response with driving distances
    resorts_with_distance = []
    for i, item in enumerate(page_resorts):
        route_info = route_infos[i]
        if route_info:
            resorts_with_distance.append(
                {
                    **item["resort"],
                    "air_distance_km": round(item["air_distance_km"], 2),
                    "distance_km": route_info["distance_km"],
                    "duration_minutes": route_info["duration_minutes"],
                }
            )

    return {
        "user_location": location.dict(),
        "page": page,
        "page_size": page_size,
        "total_resorts": len(ski_resorts),
        "has_more": end_idx < len(ski_resorts),
        "resorts": resorts_with_distance,
    }
