from pydantic import BaseModel
from datetime import date as date_type

class Location(BaseModel):
    lat: float
    lng: float


class SnowReport(BaseModel):
    pistes_km: str | None
    lifts: str | None
    snow_depth_cm: str | None
    updated_on: str | None


class WeatherPeriod(BaseModel):
    time: str
    temperature_celsius: float | None
    precipitation_mm: float | None
    snowfall_cm: float | None
    cloud_cover_percent: int | None
    visibility_m: float | None


class WeatherData(BaseModel):
    snowfall_prev_24h_cm: float | None
    morning: WeatherPeriod
    midday: WeatherPeriod
    afternoon: WeatherPeriod
    


class WeatherRequest(BaseModel):
    lat: float
    lng: float
    date: str


class SkiResort(BaseModel):
    id: str
    name: str
    location: Location
    elevation: str | None
    snowreport_url: str
    air_distance_km: float
    distance_km: float | None
    duration_driving_minutes: float | None
    duration_transit_minutes: float | None
    maps_directions_url_driving: str | None
    maps_directions_url_transit: str | None
    snow_report: SnowReport
    weather: WeatherData


class SkiResortsResponse(BaseModel):
    page: int
    page_size: int
    total_resorts: int
    has_more: bool
    resorts: list[SkiResort]
