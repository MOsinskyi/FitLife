from typing import Any

accounts_db = {}
coaches_db = {}
customers_db = {}
memberships_db = {}
booking_db = {}
schedules_db = {}


def get_db() -> dict[str, Any]:
    return {
        "accounts": accounts_db,
        "coaches": coaches_db,
        "customers": customers_db,
        "memberships": memberships_db,
        "bookings": booking_db,
        "schedules": schedules_db,
    }
