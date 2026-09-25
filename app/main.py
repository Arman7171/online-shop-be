from fastapi import FastAPI

from app.api.v1.router import api_router
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title="Shop API",
    version="1.0.0",
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)


app.include_router(
    api_router,
    prefix="/api/v1",
)