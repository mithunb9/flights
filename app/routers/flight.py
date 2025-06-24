from fastapi import APIRouter
from app.models.flight import Flight
from app.data.flightradar import get_flights as get_flights_flightradar
from typing import List

router = APIRouter()

@router.get("/flights/flightradar")
def get_flights_endpoint() -> List[Flight]:
    return get_flights_flightradar()