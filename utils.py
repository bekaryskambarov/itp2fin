from geopy.distance import geodesic

# Example coordinates for Astana spots
ASTANA_SPOTS = [
    {"name": "Bayterek Tower", "coords": (51.1283, 71.4305)},
    {"name": "Khan Shatyr", "coords": (51.1327, 71.4038)},
    {"name": "Botanical Garden", "coords": (51.1031, 71.4172)}
]

def find_nearest(user_lat, user_lon):
    user_pos = (user_lat, user_lon)
    # Sort spots by distance
    sorted_spots = sorted(
        ASTANA_SPOTS,
        key=lambda x: geodesic(user_pos, x['coords']).kilometers
    )
    return sorted_spots[0] # Returns the single closest spot