from app.cache.airline import get_icao_mapping, get_country_mapping

ICAO_MAPPING = get_icao_mapping()
COUNTRY_MAPPING = get_country_mapping()

def populate_airline(icao: str):
    return ICAO_MAPPING.get(icao)

def populate_country(icao: str):
    return COUNTRY_MAPPING.get(icao)