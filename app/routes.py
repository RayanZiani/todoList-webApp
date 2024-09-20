from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, date
from pydantic import BaseModel
from .models import Task
from .database import SessionLocal

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

# session sql alchemy
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
        due_date_parsed = date.fromisoformat(task.due_date) if task.due_date else None
        new_task = Task(title=task.title, description=task.description, due_date=due_date_parsed)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        # redirection quand ca créer task
        return RedirectResponse(url="/todo", status_code=303)
    except Exception as e:
        return JSONResponse(content={"success": False, "message": str(e)}, status_code=400)

# Route pour supprimer une tâche
@router.delete("/tasks/{task_id}/delete")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            db.delete(task)
            db.commit()
            return JSONResponse(content={"success": True, "message": "Tâche supprimée"})
        else:
            raise HTTPException(status_code=404, detail="Tâche non trouvée")
    except Exception as e:
        # Ajoute un log ici si nécessaire
        return JSONResponse(content={"success": False, "message": f"Erreur serveur: {str(e)}"}, status_code=500)

@router.get("/tasks/{task_id}")
async def get_task(task_id: int, db: Session = Depends(get_db)):
    print(f"Received task_id: {task_id}")  # Log the task ID
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        return {
            "success": True,
            "task": {
                "title": task.title,
                "due_date": task.due_date,
                "creation_date": task.creation_date,
                "description": task.description,
                "completed": task.completed,
                "completed_at": task.completed_at.strftime('%Y-%m-%d %H:%M') if task.completed_at else None
            }
        }
    else:
        print(f"Task with ID {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")

class TaskUpdateCompleted(BaseModel):
    completed: bool
@router.put("/tasks/{task_id}/complete")
async def complete_task(task_id: int, task_update: TaskUpdateCompleted, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update the completed status from the model
    task.completed = task_update.completed
    task.completed_at = datetime.utcnow() if task_update.completed else None  # Update completed_at if completed

    db.commit()
    return {"success": True, "message": "Task updated", "completed": task.completed}