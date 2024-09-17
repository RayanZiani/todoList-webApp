from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .models import tasks_db, Task

router = APIRouter()

# Configuration de Jinja2 pour utiliser les templates
templates = Jinja2Templates(directory="app/templates")

# Route pour la page web
@router.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks_db})

# Route pour ajouter une nouvelle tâche depuis le formulaire HTML
@router.post("/tasks/create")
async def create_task(title: str = Form(...), description: str = Form(None)):
    new_task = Task(id=len(tasks_db) + 1, title=title, description=description)
    tasks_db.append(new_task)
    return templates.TemplateResponse("index.html", {"request": Request, "tasks": tasks_db})
