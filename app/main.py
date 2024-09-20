from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import engine
from . import models
from .routes import router

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
# css js...
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router)
