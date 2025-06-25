from enum import Enum
from datetime import datetime

from storage import load_tasks, load_task_by_id, save_task, update_task_in_db, delete_task_by_id

class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"

def add_task(task_description) -> int:
    task = {"description": task_description, "status": TaskStatus.TODO.value, "createdAt": datetime.now().isoformat(),
            "updatedAt": None}
    return save_task(task)

def update_task(task_id: int, new_task_description: str) -> int:
    task = load_task_by_id(task_id)
    task["description"] = new_task_description
    task["updatedAt"] = datetime.now().isoformat()
    return update_task_in_db(task)

def delete_task(task_id: int) -> bool:
    return delete_task_by_id(task_id)

def mark_task_done(task_id: int) -> int:
    task = load_task_by_id(task_id)
    task["status"] = TaskStatus.DONE.value
    task["updatedAt"] = datetime.now().isoformat()
    return update_task_in_db(task)

def mark_task_in_progress(task_id: int) -> int:
    task = load_task_by_id(task_id)
    task["status"] = TaskStatus.IN_PROGRESS.value
    task["updatedAt"] = datetime.now().isoformat()
    return update_task_in_db(task)

def list_all_tasks() -> list:
    return load_tasks()

def list_all_tasks_filtered(task_status: TaskStatus) -> list:
    tasks = load_tasks()
    tasks_done = list(filter(lambda task: task["status"] == task_status.value, tasks))
    return tasks_done