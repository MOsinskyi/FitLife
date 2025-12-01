from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse

from fitlife.database import router as database_router
from fitlife.member.routers import router as member_router
from fitlife.membership.routers import router as membership_router
from fitlife.trainer.routers import router as trainer_router
from fitlife.workout_session.routers import router as workout_session_router

app = FastAPI(
    title='FitLife API',
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'success': False,
            'msg': exc.detail,
        },
    )


app.include_router(member_router)
app.include_router(trainer_router)
app.include_router(membership_router)
app.include_router(workout_session_router)
app.include_router(database_router)
