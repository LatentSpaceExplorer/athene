import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class TodoManager:
    def __init__(self, file_path="./data/todos.json"):
        self.file_path = Path(file_path)
        # Create directory if it doesn't exist
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.todos: List[Dict] = self._load_todos()

    def _load_todos(self) -> List[Dict]:
        if self.file_path.exists():
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return []

    def _save_todos(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.todos, f, indent=2)


    def add_todo(self, task_description: str, due_date: Optional[str] = None) -> str:
        task = {
            "description": task_description,
            "due_date": due_date,
            "created_at": datetime.now().isoformat()
        }
        self.todos.append(task)
        self._save_todos()
        return f"Added task: {task_description}" + (f" (Due: {due_date})" if due_date else "")


    def remove_todo(self, index: int) -> str:
        if 0 <= index < len(self.todos):
            removed = self.todos.pop(index)
            self._save_todos()
            return f"Removed task: {removed['description']}"
        return "Invalid task index"


    def list_todos(self) -> str:
        if not self.todos:
            return "You have no tasks in your todo list."
        
        formatted_tasks = []
        task_count = len(self.todos)
        
        # Add introduction
        formatted_tasks.append(f"You have {task_count} {'task' if task_count == 1 else 'tasks'} in your list:")
        
        # Format each task
        for i, task in enumerate(self.todos, 1):
            task_str = f"Task {i}: {task['description']}"
            if task.get('due_date'):
                task_str += f", due on {task['due_date']}"
            formatted_tasks.append(task_str)
        
        # Add a natural pause between tasks using periods
        return ". ".join(formatted_tasks)