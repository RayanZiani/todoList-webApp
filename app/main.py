from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import engine
from . import models
from .routes import usersRoutes, tasksRoutes, pageRoutes

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
# css js...
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Inclusion des routes séparées
app.include_router(tasksRoutes.router, prefix="/api")  # Préfixe API pour les routes CRUD des tâches
app.include_router(pageRoutes.router)  # Routes pour les pages HTML
app.include_router(usersRoutes.router, prefix="/api")

