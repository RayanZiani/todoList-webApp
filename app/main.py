from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import engine
from . import models
from .routes import router  # Importer le routeur défini dans routes.py

# Initialiser la base de données
models.Base.metadata.create_all(bind=engine)

# Créer l'instance de FastAPI
app = FastAPI()

# Monter les fichiers statiques (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Inclure les routes définies dans routes.py
app.include_router(router)
