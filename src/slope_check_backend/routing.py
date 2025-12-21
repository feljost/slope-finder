import os

import requests
from dotenv import load_dotenv

load_dotenv()

MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY")


def get_driving_distances_batch(
    origin_lat: float, origin_lng: float, destinations: list[dict]
) -> list[dict]:
    """
    Get driving distances and durations from origin to multiple destinations using Mapbox Directions Matrix API.
    Processes up to 25 destinations at a time.

    destinations should be a list of dicts with 'lat' and 'lng' keys.
    Returns list of dicts with distance_km and duration_minutes, or None for unreachable destinations.
    """
    if not MAPBOX_API_KEY:
        raise ValueError("MAPBOX_API_KEY not set in environment variables")

    # Limit to first 25 destinations
    destinations = destinations[:10]

    # Format coordinates: origin first, then all destinations
    coords = f"{origin_lng},{origin_lat}"
    for dest in destinations:
        coords += f";{dest['lng']},{dest['lat']}"

    url = f"https://api.mapbox.com/directions-matrix/v1/mapbox/driving/{coords}"

    params = {
        "access_token": MAPBOX_API_KEY,
        "sources": "0",
        "destinations": ";".join([str(i) for i in range(1, len(destinations) + 1)]),
        "annotations": "distance,duration",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    print(data)

    if not data.get("durations") or not data.get("distances"):
        return [None] * len(destinations)

    # Extract the first row (origin to all destinations)
    durations = data["durations"][0]
    distances = data["distances"][0]

    results = []
    for i in range(len(destinations)):
        if durations[i] is not None and distances[i] is not None:
            results.append({
                "distance_km": round(distances[i] / 1000, 2),
                "duration_minutes": round(durations[i] / 60, 1),
            })
        else:
            results.append(None)

    return results
