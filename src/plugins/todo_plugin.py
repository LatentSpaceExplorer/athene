from typing import Dict, List, Optional
from .base import Plugin
from pydantic import BaseModel, Field
from datetime import datetime
import json
from pathlib import Path


class AddTask(BaseModel):
    """Add a new task to the todo list."""
    task_description: str = Field(..., description="The description of the task to add")
    due_date: Optional[str] = Field(None, description="Optional due date for the task")

class DeleteTask(BaseModel):
    """Delete a task from the todo list."""
    task_id: int = Field(..., description="The ID of the task to delete")

class ListTasks(BaseModel):
    """List all tasks in the todo list."""


class TodoPlugin(Plugin):
    def __init__(self, file_path="./data/todos.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.todos: List[Dict] = self._load_todos()
    
    @property
    def name(self) -> str:
        return "todo manager"
    
    def get_tools(self):
        return [AddTask, DeleteTask, ListTasks]
    
    def execute_tool(self, tool_name: str, **kwargs) -> str:
        if tool_name == "AddTask":
            return self._add_task(**kwargs)
        elif tool_name == "DeleteTask":
            return self._delete_task(**kwargs)
        elif tool_name == "ListTasks":
            return self._list_tasks()
        raise ValueError(f"Unknown tool: {tool_name}")

    def _load_todos(self) -> List[Dict]:
        """Load todos from file"""
        if self.file_path.exists():
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return []

    def _save_todos(self):
        """Save todos to file"""
        with open(self.file_path, 'w') as f:
            json.dump(self.todos, f, indent=2)

    def _add_task(self, task_description: str, due_date: Optional[str] = None) -> str:
        """Add a new task to the todo list"""
        task = {
            "description": task_description,
            "due_date": due_date,
            "created_at": datetime.now().isoformat()
        }
        self.todos.append(task)
        self._save_todos()
        return f"Added task: {task_description}" + (f" (Due: {due_date})" if due_date else "")

    def _delete_task(self, task_id: int) -> str:
        """Delete a task from the todo list"""
        index = task_id - 1  # Convert to 0-based index
        if 0 <= index < len(self.todos):
            removed = self.todos.pop(index)
            self._save_todos()
            return f"Removed task: {removed['description']}"
        return "Invalid task index"

    def _list_tasks(self) -> str:
        """List all tasks in the todo list"""
        if not self.todos:
            return "No tasks found."
        
        task_list = []
        for i, task in enumerate(self.todos, 1):
            task_str = f"{i}. {task['description']}"
            if task.get('due_date'):
                task_str += f" (Due: {task['due_date']})"
            task_list.append(task_str)
            
        return "\n".join(task_list) 