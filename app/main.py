from fastapi import FastAPI, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from .database import SessionLocal, engine
from . import models

# Initialiser la base de données
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuration de Jinja2 pour utiliser les templates
templates = Jinja2Templates(directory="app/templates")

# Configuration des fichiers statiques
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Dépendance pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route pour la page HTML
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

# Route pour ajouter une nouvelle tâche
@app.post("/tasks/create")
async def create_task(title: str = Form(...), description: str = Form(None), db: Session = Depends(get_db)):
    task = models.Task(title=title, description=description)
    db.add(task)
    db.commit()
    db.refresh(task)
    tasks = db.query(models.Task).all()
    return templates.TemplateResponse("index.html", {"request": Request, "tasks": tasks})
