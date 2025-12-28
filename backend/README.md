<div align="center">

# Slope Finder (Backend)

FastAPI backend for finding and ranking Swiss ski resorts based on location.

## API Endpoints

### GET `/resorts-info`
Returns paginated ski resorts sorted by distance.

**Parameters:**
- `lat` (float): User latitude
- `lng` (float): User longitude
- `date` (string): Date for weather data (YYYY-MM-DD format)
- `page` (int): Page number (default: 1)
- `page_size` (int): Results per page (max: 10, default: 10)

**Response:**
```json
{
  "page": 1,
  "page_size": 10,
  "total_resorts": 60,
  "has_more": true,
  "resorts": [
    {
      "id": "zermatt",
      "name": "Zermatt",
      "location": {"lat": 46.0207, "lng": 7.7491},
      "elevation": "1620m - 3883m",
      "snowreport_url": "...",
      "air_distance_km": 45.2,
      "distance_km": 67.8,
      "duration_minutes": 52,
      "snow_report": {...},
      "weather": {...}
    },
    ...
  ]
}
```

## Usage

Set your GOOGLE_ROUTES_API_KEY in the .env file.

Next, you can run the backend with `uv`

```shell
uv venv
uv pip install -e .
```
Then start the server with uv:
```bash
uv run dev
```
Or with uvicorn:

``` 
uvicorn slope_finder_be.api.main:app
```


If you want to deploy it, you may use the `Dockerfile`. It is currently setup for Google Cloud Run.