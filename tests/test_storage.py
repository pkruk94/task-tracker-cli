import os
import tempfile
import pytest

import storage

@pytest.fixture
def  temp_tasks_file(monkeypatch):
    import tempfile, os
    tmp = tempfile.NamedTemporaryFile(delete=False)
    fname = tmp.name
    tmp.close()
    monkeypatch.setattr(storage, "FILENAME", fname)
    yield fname
    if os.path.exists(fname):
        os.remove(fname)

def test_load_tasks_empty_file(temp_tasks_file):
    tasks = storage.load_tasks()
    assert len(tasks) == 0

def test_save_and_load_task(temp_tasks_file):
    task = {"description": "Test task", "status": "todo", "createdAt": "2024-06-25T14:00", "updatedAt": None}
    task_id = storage.save_task(task)
    tasks = storage.load_tasks()
    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id
    assert tasks[0]["description"] == "Test task"

def test_load_tasks_by_id(temp_tasks_file):
    task = {"description": "Test task2", "status": "todo", "createdAt": "2024-06-25T14:10", "updatedAt": None}
    task_id = storage.save_task(task)
    loaded_tasks = storage.load_task_by_id(task_id)
    assert loaded_tasks["id"] == task_id
    assert loaded_tasks["description"] == "Test task2"

def test_update_task_in_db(temp_tasks_file):
    task = {"description": "To update", "status": "todo", "createdAt": "2024-06-25T14:20", "updatedAt": None}
    task_id = storage.save_task(task)
    task_to_update = storage.load_task_by_id(task_id)
    task_to_update["description"] = "Updated!"
    storage.update_task_in_db(task_to_update)
    updated_task = storage.load_task_by_id(task_id)
    assert updated_task["description"] == "Updated!"

def test_delete_task_by_id(temp_tasks_file):
    task = {"description": "To delete", "status": "todo", "createdAt": "2024-06-25T14:30", "updatedAt": None}
    task_id = storage.save_task(task)
    assert len(storage.load_tasks()) == 1
    storage.delete_task_by_id(task_id)
    assert storage.load_tasks() == []

def test_find_task_id_in_list(temp_tasks_file):
    t1 = {"description": "A", "status": "todo", "createdAt": "2024-06-25T14:40", "updatedAt": None}
    t2 = {"description": "B", "status": "todo", "createdAt": "2024-06-25T14:41", "updatedAt": None}
    id1 = storage.save_task(t1)
    id2 = storage.save_task(t2)
    tasks = storage.load_tasks()
    idx_to_check = storage.find_task_id_in_list(id2, tasks)
    assert tasks[idx_to_check]["id"] == id2

def test_load_task_by_id_not_found(temp_tasks_file):
    with pytest.raises(ValueError):
        storage.load_task_by_id(9999)

def test_delete_task_by_id_not_found(temp_tasks_file):
    with pytest.raises(ValueError):
        storage.delete_task_by_id(9999)

def test_update_task_in_db_not_found(temp_tasks_file):
    fake_task = {"id": 12345, "description": "X", "status": "todo", "createdAt": "2024-06-25T14:00", "updatedAt": None}
    with pytest.raises(ValueError):
        storage.update_task_in_db(fake_task)

def test_generate_new_id(temp_tasks_file):
    t1 = {"description": "A", "status": "todo", "createdAt": "2024-06-25T14:50", "updatedAt": None}
    t2 = {"description": "B", "status": "todo", "createdAt": "2024-06-25T14:51", "updatedAt": None}
    id1 = storage.save_task(t1)
    id2 = storage.save_task(t2)
    assert id2 == id1 + 1
    next_id = storage.generate_new_id()
    assert next_id == id2 + 1