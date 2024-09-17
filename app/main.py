from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routes import router

app = FastAPI()

# Inclure les routes définies dans routes.py
app.include_router(router)

# Servir les fichiers statiques (CSS, images, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Route racine pour l'API (pour tester rapidement que l'API fonctionne toujours)
@app.get("/api/")
async def root():
    return {"message": "Welcome to the ToDo List API"}
