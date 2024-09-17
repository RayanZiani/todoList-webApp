from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .models import Task
from .database import SessionLocal

# Créer l'instance du routeur
router = APIRouter()

# Configuration de Jinja2 pour utiliser les templates
templates = Jinja2Templates(directory="app/templates")

# Dépendance pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route pour afficher la page d'accueil avec la liste des tâches
@router.get("/", response_class=HTMLResponse)
async def get_home(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

# Route pour ajouter une nouvelle tâche depuis le formulaire HTML
@router.post("/tasks/create")
async def create_task(title: str = Form(...), description: str = Form(None), db: Session = Depends(get_db)):
    new_task = Task(title=title, description=description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    tasks = db.query(Task).all()  # Récupérer la liste des tâches après ajout
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})
