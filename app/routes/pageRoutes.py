from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from ..models import Task
from ..database import get_db
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from ..token import verify_token
from jose import JWTError

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

# Set up OAuth2PasswordBearer for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Dependency to check if the user is authenticated (used only in API routes)
def get_current_user(token: str = Depends(oauth2_scheme)):
    print(f"Token received in get_current_user: {token}")  # Debugging

    if not token:
        print("No token found, raising HTTPException")
        raise HTTPException(status_code=401, detail="Token not provided")

    try:
        payload = verify_token(token)
        print(f"Token payload: {payload}")  # Debugging
        return payload
    except JWTError as e:
        print(f"JWT Error: {e}")  # Debugging
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# Public route: Login page (no token required)
@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Public route: Home page (no authentication required for HTML)
@router.get("/", response_class=HTMLResponse)
async def get_home(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

# Protected API route: Fetch home data (requires token)
@router.get("/api/home-data")
async def get_home_data():
    return


# Public route: Dashboard page (no authentication required for HTML)
@router.get("/dash", response_class=HTMLResponse)
async def get_dashboard(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return templates.TemplateResponse("dashboard.html", {"request": request})
# Protected API route: Fetch dashboard data (requires token)
@router.get("/api/dash-data")
async def get_dashboard_data():
    return



# Public route: Add task page (no authentication required for HTML)
@router.get("/add", response_class=HTMLResponse)
async def get_add_task_page(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})
@router.get("/api/add-data")
async def get_add_data():
    return


# Public route: ToDo page (no authentication required for HTML)
@router.get("/todo", response_class=HTMLResponse)
async def get_todo_page(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return templates.TemplateResponse("todo.html", {"request": request, "tasks": tasks})
# Protected API route: Fetch ToDo data (requires token)
@router.get("/api/todo-data")
async def get_todo_data(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    tasks = db.query(Task).all()  # Fetch all tasks from the database

    # Convert tasks into a JSON-friendly format
    task_list = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
            "completed": task.completed,
            "completed_at": task.completed_at.strftime('%Y-%m-%d %H:%M') if task.completed_at else None
        }
        for task in tasks
    ]

    return

# Public route: Plans page (no authentication required for HTML)
@router.get("/plans", response_class=HTMLResponse)
async def get_plans_page(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).all()  # If tasks are needed, otherwise remove
    return templates.TemplateResponse("plans.html", {"request": request})

# Protected API route: Fetch Plans data (requires token)
@router.get("/api/plans-data")
async def get_plans_data():
    return

# Public route: Settings page (no authentication required for HTML)
@router.get("/settings", response_class=HTMLResponse)
async def get_settings_page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("settings.html", {"request": request})

# Protected API route: Fetch Settings data (requires token)
@router.get("/api/settings-data")
async def get_settings_data():
    return
