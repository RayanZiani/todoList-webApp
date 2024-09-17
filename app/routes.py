from fastapi import APIRouter, HTTPException
from .models import tasks_db, Task
from .schemas import TaskCreate, TaskResponse

router = APIRouter()

# Route pour obtenir toutes les tâches
@router.get("/tasks/", response_model=list[TaskResponse])
async def get_tasks():
    return tasks_db

# Route pour créer une nouvelle tâche
@router.post("/tasks/", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    new_task = Task(id=len(tasks_db) + 1, title=task.title, description=task.description)
    tasks_db.append(new_task)
    return new_task

# Route pour obtenir une tâche par son ID
@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    task = next((task for task in tasks_db if task.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
