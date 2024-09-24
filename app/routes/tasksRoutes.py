from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, date
from pydantic import BaseModel
from ..models import Task, User
from ..database import get_db
from ..auth import get_current_user

router = APIRouter()



# Modèle Pydantic pour valider les données JSON lors de la création d'une tâche
class TaskCreate(BaseModel):
    title: str
    description: str = None
    due_date: str = None  # Date sous forme de chaîne

class TaskUpdateCompleted(BaseModel):
    completed: bool

# Route pour ajouter une nouvelle tâche via JSON
@router.post("/tasks/create")
async def create_task(task: TaskCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    print(
        f"Creating task for user: {user.nom} (ID: {user.uid})")  # Log pour s'assurer que l'utilisateur est bien récupéré
    try:
        # Parse la date si elle existe
        due_date_parsed = date.fromisoformat(task.due_date) if task.due_date else None

        # Créer la nouvelle tâche
        new_task = Task(
            title=task.title,
            description=task.description,
            due_date=due_date_parsed,
            user_id=user.uid  # Associe la tâche à l'utilisateur connecté
        )

        # Ajouter la tâche dans la base de données
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        # Retourner la tâche créée
        return JSONResponse(content={
            "success": True,
            "task": {
                "id": new_task.id,
                "title": new_task.title,
                "description": new_task.description,
                "due_date": new_task.due_date.strftime('%Y-%m-%d') if new_task.due_date else None
            }
        })

    except Exception as e:
        print(f"Error creating task: {str(e)}")  # Log pour voir l'erreur exacte
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")


# Route pour supprimer une tâche

@router.delete("/tasks/{task_id}/delete")
async def delete_task(task_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Vérifiez que la tâche appartient à l'utilisateur connecté
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.uid).first()

    if not task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée ou vous n'avez pas accès à cette tâche")

    # Supprimez la tâche
    db.delete(task)
    db.commit()
    return JSONResponse(content={"success": True, "message": "Tâche supprimée avec succès"})

@router.get("/tasks/{task_id}")
async def get_task(task_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    print(f"Received task_id: {task_id} from user: {user.uid}")  # Log the task ID and user ID

    # Chercher la tâche qui correspond à l'ID et appartient à l'utilisateur connecté
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.uid).first()

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
        print(f"Task with ID {task_id} not found for user {user.uid}")
        raise HTTPException(status_code=404, detail="Task not found or you don't have access to it")


class TaskUpdateCompleted(BaseModel):
    completed: bool


@router.put("/tasks/{task_id}/complete")
async def complete_task(task_id: int, task_update: TaskUpdateCompleted, db: Session = Depends(get_db),
                        user: User = Depends(get_current_user)):
    # Vérifiez que la tâche appartient à l'utilisateur connecté
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.uid).first()

    if not task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée ou vous n'avez pas accès à cette tâche")

    # Mettre à jour le statut "completed" de la tâche
    task.completed = task_update.completed
    task.completed_at = datetime.utcnow() if task_update.completed else None  # Mettre à jour completed_at si terminé

    db.commit()
    return {"success": True, "message": "Statut de la tâche mis à jour", "completed": task.completed}


@router.get("/tasks")
async def get_user_tasks(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Récupérer toutes les tâches qui appartiennent à l'utilisateur connecté
    tasks = db.query(Task).filter(Task.user_id == user.uid).all()

    tasks_list = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date,
            "creation_date": task.creation_date,
            "completed": task.completed,
            "completed_at": task.completed_at.strftime('%Y-%m-%d %H:%M') if task.completed_at else None
        }
        for task in tasks
    ]

    return {
        "success": True,
        "tasks": tasks_list
    }