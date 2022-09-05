from fastapi import FastAPI
from app.api.api_v1.api import api_router
from app.core.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIP,
    version=settings.APP_VERSION,
    contact=settings.APP_CONTACT,
    license_info=settings.APP_LICENSE
)

app.include_router(
    api_router,
    prefix=settings.API_V1_STR
)