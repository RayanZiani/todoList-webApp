from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from ..models import Task
from ..database import get_db
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

# Route pour afficher la page login
@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Route pour afficher la page d'accueil
@router.get("/", response_class=HTMLResponse)
async def get_home(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

# Route pour afficher le tableau de bord
@router.get("/dash", response_class=HTMLResponse)
async def get_dashboard(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "tasks": tasks})

# Route pour la page "Ajouter une tâche"
@router.get("/add", response_class=HTMLResponse)
async def get_add_task(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})

# Route pour la page ToDo
@router.get("/todo", response_class=HTMLResponse)
async def get_todo_page(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return templates.TemplateResponse("todo.html", {"request": request, "tasks": tasks})

# Autres routes pour plans, paramètres...
@router.get("/plans", response_class=HTMLResponse)
async def get_plans(request: Request):
    return templates.TemplateResponse("plans.html", {"request": request})

@router.get("/settings", response_class=HTMLResponse)
async def get_settings(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})