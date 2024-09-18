from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date
from pydantic import BaseModel
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

# Modèle Pydantic pour valider les données JSON lors de la création d'une tâche
class TaskCreate(BaseModel):
    title: str
    description: str = None
    due_date: str = None  # Date sous forme de chaîne

# Route pour afficher la page d'accueil avec la liste des tâches
@router.get("/", response_class=HTMLResponse)
async def get_home(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

# Route pour la page Ajouter une tâche (add.html)
@router.get("/add", response_class=HTMLResponse)
async def get_add(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})

# Route pour la page ToDo (todo.html)
@router.get("/todo", response_class=HTMLResponse)
async def get_todo(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return templates.TemplateResponse("todo.html", {"request": request, "tasks": tasks})

# Route pour ajouter une nouvelle tâche via JSON
@router.post("/tasks/create")
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    try:
        # Convertir la chaîne due_date en objet date si elle est fournie
        due_date_parsed = date.fromisoformat(task.due_date) if task.due_date else None

        # Créer la nouvelle tâche avec les données reçues
        new_task = Task(title=task.title, description=task.description, due_date=due_date_parsed)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        # Rediriger vers la page ToDo après la création de la tâche
        return RedirectResponse(url="/todo", status_code=303)
    except Exception as e:
        return JSONResponse(content={"success": False, "message": str(e)}, status_code=400)

# Route pour supprimer une tâche
@router.delete("/tasks/{task_id}/delete")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return JSONResponse(content={"success": True, "message": "Tâche supprimée"})
    else:
        return JSONResponse(content={"success": False, "message": "Tâche non trouvée"}, status_code=404)
