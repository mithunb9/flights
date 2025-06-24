from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Flight(BaseModel):
    callsign: str
    flight_number: str
    latitude: float
    longitude: float
    altitude: int
    ground_speed: int
    vertical_rate: int
    registration: str
    origin_icao: Optional[str] = None
    destination_icao: Optional[str] = None
    origin_iata: Optional[str] = None
    destination_iata: Optional[str] = None
    eta: Optional[datetime]