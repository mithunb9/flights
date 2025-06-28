from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Flight(BaseModel):
    callsign: str 
    flight_number: str
    airline: str
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[int] = None
    ground_speed: Optional[int] = None
    vertical_rate: Optional[int] = None
    registration: Optional[str] = None
    origin_icao: Optional[str] = None
    destination_icao: Optional[str] = None
    origin_iata: Optional[str] = None
    destination_iata: Optional[str] = None
    eta: Optional[datetime] = None
