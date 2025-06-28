from fastapi import APIRouter
from app.models.flight import Flight
from app.data.flightradar import get_flights as get_flights_flightradar
from typing import List
from app.data.location import get_bounds_from_lat_long

router = APIRouter()

@router.get("/flights/flightradar")
def get_flights_endpoint(lat: float = None, long: float = None) -> List[Flight]:
    if lat and long:
        bounds = get_bounds_from_lat_long(lat, long)
        return get_flights_flightradar(bounds)
    
    return get_flights_flightradar()