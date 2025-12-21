from pydantic import BaseModel
from datetime import date as date_type

class Location(BaseModel):
    lat: float
    lng: float


class SnowReport(BaseModel):
    pistes_km: str
    lifts: str
    snow_depth_cm: str
    updated_on: str


class WeatherPeriod(BaseModel):
    time: str
    temperature_celsius: float
    precipitation_mm: float
    snowfall_cm: float
    cloud_cover_percent: int
    visibility_m: float


class WeatherData(BaseModel):
    snowfall_prev_24h_cm: float
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
    elevation: str
    snowreport_url: str
    air_distance_km: float
    distance_km: float
    duration_minutes: float
    snow_report: SnowReport
    weather: WeatherData


class SkiResortsResponse(BaseModel):
    page: int
    page_size: int
    total_resorts: int
    has_more: bool
    resorts: list[SkiResort]
