from typing import List

class Task:
    def __init__(self, id: int, title: str, description: str = None):
        self.id = id
        self.title = title
        self.description = description

# On crée une liste de tâches en tant que base de données temporaire
tasks_db: List[Task] = []