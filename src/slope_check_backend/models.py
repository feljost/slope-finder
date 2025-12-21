from pydantic import BaseModel


class LocationQuery(BaseModel):
    lat: float
    lng: float
