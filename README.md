<div align="center">

# Slope Finder (Backend)

**Find the perfect ski resort based on your location and travel dates**

[![Website](https://img.shields.io/badge/Website-slopefinder.ch-blue?style=for-the-badge)](https://slopefinder.ch)
[![Frontend](https://img.shields.io/badge/Backend-Repository-green?style=for-the-badge&logo=github)](https://github.com/feljost/slope-finder-fe)

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-DE5FE9?style=flat-square&logo=uv&logoColor=white)](https://docs.astral.sh/uv/)

</div>

---
FastAPI backend for finding and ranking Swiss ski resorts based on location.

## Features

- **Distance Calculation**: Calculates both air and driving distances from user location
- **Snow Reports**: Live snow depth, piste status, and lift information
- **Weather Data**: 24h snowfall, temperature, precipitation, and visibility forecasts
- **Pagination**: Supports infinite scrolling with configurable page size

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

Locally you can run the backend with `uv`

```shell
uv venv
uv pip install -e .
uvicorn slope_finder_be.api.main:app
```

If you want to deploy it, you may use the `Dockerfile`. It is currently setup for Google Cloud Run.