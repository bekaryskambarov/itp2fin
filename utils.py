from geopy.distance import geodesic


def calculate_nearest_places(user_lat, user_lon, all_places, limit=5):
    """
    Calculates distance from user to all places and returns the top N closest.
    """
    user_pos = (user_lat, user_lon)

    # Add distance key to every dictionary in the list
    for place in all_places:
        place_pos = (place['lat'], place['lon'])
        place['distance'] = geodesic(user_pos, place_pos).kilometers

    # Sort by distance (ascending)
    sorted_places = sorted(all_places, key=lambda x: x['distance'])
    return sorted_places[:limit]


def format_feedback(reviews):
    """Formats a list of reviews into a clean string."""
    if not reviews:
        return "No feedback yet! Be the first to leave one."
    return "\n".join([f"• {r}" for r in reviews])