from typing import Any

accounts_db: dict[str, Any] = {}
coaches_db: dict[str, Any] = {}
customers_db: dict[str, Any] = {}
memberships_db: dict[str, Any] = {}
booking_db: dict[str, Any] = {}
schedules_db: dict[str, Any] = {}


def get_db() -> dict[str, Any]:
    return {
        "accounts": accounts_db,
        "coaches": coaches_db,
        "customers": customers_db,
        "memberships": memberships_db,
        "bookings": booking_db,
        "schedules": schedules_db,
    }
