from fastapi import FastAPI
from app.api.api_v1.api import api_router
from app.core.config import settings

from app.db.sessions import engine
from app.models import users

users.Base.metadata.create_all(bind=engine)


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