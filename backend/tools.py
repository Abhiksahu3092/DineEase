# backend/tools.py
import json, datetime, uuid, os
from backend.db import add_reservation, get_reservations_for

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/restaurants.json")


def load_restaurants():
    with open(DATA_PATH) as f:
        return json.load(f)


RESERVATIONS = []


def search_restaurants(
    area=None,
    cuisine=None,
    ambience=None,
    min_rating=0.0,
    min_capacity=1,
    name=None,
    **kwargs,
):
    """
    Safe search function that handles missing fields and extra LLM arguments.
    Added name parameter to search by restaurant name.
    """

    # Normalize min_rating safely
    try:
        min_rating = float(min_rating) if min_rating is not None else 0.0
    except:
        min_rating = 0.0

    # Normalize min_capacity safely
    try:
        min_capacity = int(min_capacity) if min_capacity is not None else 1
    except:
        min_capacity = 1

    rs = load_restaurants()
    results = []

    for r in rs:
        # Safe rating
        rating = r.get("rating", 0)
        if rating is None:
            rating = 0

        # Safe capacity
        capacity = r.get("capacity", 0)
        if capacity is None:
            capacity = 0

        # Filters
        if name and name.lower() not in r["name"].lower():
            continue

        if area and area.lower() not in r["area"].lower():
            continue

        if cuisine and cuisine.lower() not in r["cuisine"].lower():
            continue

        if ambience and ambience.lower() not in r.get("ambience", "").lower():
            continue

        if rating < min_rating:
            continue

        if capacity < min_capacity:
            continue

        results.append(r)

    return results


def check_availability(restaurant_id, date, time, party_size):
    rs = load_restaurants()
    r = next((x for x in rs if x["id"] == restaurant_id), None)

    if not r:
        return {"available": False, "reason": "unknown_restaurant"}

    cap = r["capacity"]

    # Fetch from DB
    existing = get_reservations_for(restaurant_id, date, time)
    used = sum(res["party_size"] for res in existing)

    if used + party_size <= cap:
        return {"available": True}
    else:
        return {"available": False, "reason": "full"}


def book_table(restaurant_id, name, phone, date, time, party_size):
    # First check if restaurant exists
    rs = load_restaurants()
    restaurant = next((x for x in rs if x["id"] == restaurant_id), None)

    if not restaurant:
        return {
            "success": False,
            "reason": "Restaurant not found. Please search for restaurants first to get the correct restaurant_id.",
        }

    avail = check_availability(restaurant_id, date, time, party_size)

    if not avail.get("available"):
        reason = avail.get("reason")
        if reason == "unknown_restaurant":
            return {"success": False, "reason": "Restaurant not found"}
        elif reason == "full":
            return {
                "success": False,
                "reason": f"{restaurant['name']} is fully booked at that time",
            }
        return {"success": False, "reason": reason}

    reservation_id = str(uuid.uuid4())[:8]

    res_obj = {
        "id": reservation_id,
        "restaurant_id": restaurant_id,
        "restaurant_name": restaurant["name"],
        "name": name,
        "phone": phone,
        "date": date,
        "time": time,
        "party_size": party_size,
        "status": "CONFIRMED",
    }

    add_reservation(res_obj)

    return {"success": True, "reservation": res_obj, "restaurant": restaurant}


def get_recommendations(preferences, party_size, date, time):
    """
    Simple recommendation engine:
    Score restaurants based on cuisine, area, ambience, budget, rating.
    """
    rs = load_restaurants()
    scored = []

    pref_cuisine = preferences.get("cuisine")
    pref_area = preferences.get("area")
    pref_budget = preferences.get("budget")
    pref_ambience = preferences.get("ambience")

    for r in rs:
        score = 0

        # Cuisine match
        if pref_cuisine and pref_cuisine.lower() in r["cuisine"].lower():
            score += 3

        # Area match
        if pref_area and pref_area.lower() in r["area"].lower():
            score += 2

        # Ambience match
        if pref_ambience and pref_ambience.lower() in r.get("ambience", "").lower():
            score += 2

        # Rating (always count)
        score += r["rating"]

        # Budget
        if pref_budget and r["avg_spend"] <= pref_budget:
            score += 1

        # Must satisfy party size
        if r["capacity"] >= party_size:
            score += 2
        else:
            continue  # skip restaurants too small

        scored.append((score, r))

    # Sort restaurants by score (descending)
    scored.sort(key=lambda x: x[0], reverse=True)

    # Return the top 5 recommendations
    return [item[1] for item in scored[:5]]
