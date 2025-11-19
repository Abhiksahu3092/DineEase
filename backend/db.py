from tinydb import TinyDB, Query
import os

# Compute project root from this file's location
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Point to the /data folder at project root
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)  # ensure data/ exists

# reservations.json file path inside data/
DB_PATH = os.path.join(DATA_DIR, "reservations.json")

# Initialize TinyDB
db = TinyDB(DB_PATH)
reservations = db.table("reservations")


def add_reservation(res_obj):
    result = reservations.insert(res_obj)
    return result


def get_reservations_for(restaurant_id, date, time):
    Reservation = Query()
    return reservations.search(
        (Reservation.restaurant_id == restaurant_id)
        & (Reservation.date == date)
        & (Reservation.time == time)
    )


def get_all_reservations():
    return reservations.all()


def clear_all():
    reservations.truncate()
