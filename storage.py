import json
import os
from typing import List

FILENAME = "tasks.json"

def load_tasks() -> List[dict]:
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as f:
        return json.load(f)

def load_task_by_id(task_id: int) -> dict:
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise ValueError(f"Task with id {task_id} not found")

def generate_new_id() -> int:
    tasks = load_tasks()
    if not tasks:
        return 1
    return max([task["id"] for task in tasks]) + 1

def save_task(task: dict) -> int:
    new_id = generate_new_id()
    task["id"] = new_id
    tasks = load_tasks()
    tasks.append(task)
    with open(FILENAME, "w") as f:
        json.dump(tasks, f, indent=4)
    return new_id

def update_task_in_db(task: dict) -> int:
    tasks = load_tasks()
    task_id_in_list = find_task_id_in_list(task["id"], tasks)
    tasks[task_id_in_list] = task
    with open(FILENAME, "w") as f:
        json.dump(tasks, f, indent=4)
    return task["id"]

def delete_task_by_id(task_id: int) -> bool:
    tasks = load_tasks()
    task_id_in_list = find_task_id_in_list(task_id, tasks)
    tasks.pop(task_id_in_list)
    with open(FILENAME, "w") as f:
        json.dump(tasks, f, indent=4)
    return True

def find_task_id_in_list(task_id: int, tasks: List[dict]) -> int:
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            return i
    raise ValueError("Task with id {} not found".format(task_id))