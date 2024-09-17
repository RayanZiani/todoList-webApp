from fastapi import FastAPI
from .routes import router

app = FastAPI()

app.include_router(router)

# Route racine pour vérifier que l'API fonctionne
@app.get("/")
async def root():
    return {"message": "Welcome to the ToDo List API"}