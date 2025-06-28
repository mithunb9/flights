from re import I
import requests
from app.config import settings
from fastapi import HTTPException
from app.models.flight import Flight
from datetime import datetime
from app.data.airline import populate_airline, populate_country

FLIGHT_RADAR_URL = "https://fr24api.flightradar24.com/api/"
FLIGHT_POSITIONS_FULL_ENDPOINT = "live/flight-positions/full"
USAGE_ENDPOINT = "usage"
FLIGHT_RADAR_HEADERS = {
    'Accept': 'application/json',
    'Accept-Version': 'v1',
    'Authorization': f"Bearer {settings.FLIGHT_RADAR_TOKEN}"
}

def get_flights(bounds: str = settings.DEFAULT_BOUNDS):
    PARAMS = {
        'limit': 10
    }

    if bounds:
        PARAMS['bounds'] = bounds
    
    response = requests.get(FLIGHT_RADAR_URL + FLIGHT_POSITIONS_FULL_ENDPOINT, headers=FLIGHT_RADAR_HEADERS, params=PARAMS)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json()) 
        
    flights_data = response.json().get('data', [])
    flights = []

    if not flights_data:
        return []

    for flight in flights_data:
        callsign = flight.get('callsign', '')
        flight_number = flight.get('flight', '')
        airline = populate_airline(flight.get('operating_as', ''))
        country = populate_country(flight.get('operating_as', ''))

        if not callsign or not flight_number or not airline:
            continue
        
        latitude = flight.get('lat', 0)
        longitude = flight.get('lon', 0)
        altitude = flight.get('alt', 0)
        ground_speed = flight.get('gs', 0)
        vertical_rate = flight.get('vertical_rate', 0)
        registration = flight.get('registration', '')
        origin_icao = flight.get('orig_icao', '')
        destination_icao = flight.get('dest_icao', '')
        origin_iata = flight.get('orig_iata', '')
        destination_iata = flight.get('dest_iata', '')
        eta = flight.get('eta', '')
        eta = datetime.strptime(eta, '%Y-%m-%dT%H:%M:%SZ') if eta else None

        flights.append(Flight(
            callsign=callsign, 
            flight_number=flight_number,
            airline=airline,
            country=country,
            latitude=latitude, 
            longitude=longitude, 
            altitude=altitude, 
            ground_speed=ground_speed, 
            vertical_rate=vertical_rate, 
            registration=registration, 
            origin_icao=origin_icao, 
            destination_icao=destination_icao, 
            origin_iata=origin_iata, 
            destination_iata=destination_iata, 
            eta=eta
        ))
    
    return flights

def get_usage():
    response = requests.get(FLIGHT_RADAR_URL + USAGE_ENDPOINT, headers=FLIGHT_RADAR_HEADERS)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()['data']