from fastapi import APIRouter

from fitlife.auth import views as auth
from fitlife.booking import views as booking
from fitlife.coach import views as coach
from fitlife.customer import views as customer
from fitlife.schedule import views as schedule
from fitlife.user import views as user

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(customer.router, prefix="/customers", tags=["Customers"])
api_router.include_router(coach.router, prefix="/coaches", tags=["Coaches"])
api_router.include_router(user.router, prefix="/managers", tags=["Managers"])
api_router.include_router(schedule.router, prefix="/schedules", tags=["Schedules"])
api_router.include_router(booking.router, prefix="/bookings", tags=["Bookings"])
