import math

def get_bounds_from_lat_long(lat: float, long: float, radius_km: float = 40) -> str:
    earth_radius_km = 6371.0

    delta_lat = math.degrees(radius_km / earth_radius_km)
    delta_long = math.degrees(radius_km / (earth_radius_km * math.cos(math.radians(lat))))

    north = lat + delta_lat
    south = lat - delta_lat
    east = long + delta_long
    west = long - delta_long

    return f'{north:.6f},{south:.6f},{west:.6f},{east:.6f}'

