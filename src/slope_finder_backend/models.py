from pydantic import BaseModel

class Location(BaseModel):
    lat: float
    lng: float


class SnowReport(BaseModel):
    pistes_km: str
    lifts: str
    snow_cm: str
    updated_on: str


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


class SkiResortsResponse(BaseModel):
    user_location: Location
    page: int
    page_size: int
    total_resorts: int
    has_more: bool
    resorts: list[SkiResort]
