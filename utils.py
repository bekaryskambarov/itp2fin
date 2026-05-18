from geopy.distance import geodesic

def calculate_nearest_places(user_lat, user_lon, all_places, limit=5):
    """
    Computes absolute distance metrics via geopy.
    Mutates/Adds distance key dynamically onto localized result arrays.
    """
    user_pos = (user_lat, user_lon)
    processed_list = []

    for p in all_places:
        # Convert dictionary row to editable item
        item = dict(p)
        place_pos = (item['lat'], item['lon'])
        item['distance'] = geodesic(user_pos, place_pos).kilometers
        processed_list.append(item)

    # Ascending sort logic
    sorted_places = sorted(processed_list, key=lambda x: x['distance'])
    return sorted_places[:limit]

def format_feedback(reviews):
    if not reviews:
        return "No feedback left yet. Be the first to add your experience!"
    return "\n".join([f"• {r}" for r in reviews])