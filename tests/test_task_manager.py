import os
import tempfile
import pytest

import storage
import task_manager

@pytest.fixture
def temp_tasks_file(monkeypatch):
    import tempfile, os
    tmp = tempfile.NamedTemporaryFile(delete=False)
    fname = tmp.name
    tmp.close()
    monkeypatch.setattr(storage, "FILENAME", fname)
    yield fname
    if os.path.exists(fname):
        os.remove(fname)

def test_add_task(temp_tasks_file):
    task_id = task_manager.add_task("Do homework")
    tasks = task_manager.list_all_tasks()
    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id
    assert tasks[0]["description"] == "Do homework"
    assert tasks[0]["status"] == task_manager.TaskStatus.TODO.value

def test_update_task(temp_tasks_file):
    task_id = task_manager.add_task("Old description")
    task_manager.update_task(task_id, "New description")
    task = storage.load_task_by_id(task_id)
    assert task["description"] == "New description"
    assert task["updatedAt"] is not None

def test_delete_task(temp_tasks_file):
    task_id = task_manager.add_task("To be deleted")
    assert len(task_manager.list_all_tasks()) == 1
    task_manager.delete_task(task_id)
    assert task_manager.list_all_tasks() == []

def test_mark_task_done(temp_tasks_file):
    task_id = task_manager.add_task("Finish project")
    task_manager.mark_task_done(task_id)
    task = storage.load_task_by_id(task_id)
    assert task["status"] == task_manager.TaskStatus.DONE.value
    assert task["updatedAt"] is not None

def test_mark_task_in_progress(temp_tasks_file):
    task_id = task_manager.add_task("Prepare report")
    task_manager.mark_task_in_progress(task_id)
    task = storage.load_task_by_id(task_id)
    assert task["status"] == task_manager.TaskStatus.IN_PROGRESS.value
    assert task["updatedAt"] is not None

def test_list_all_tasks_filtered(temp_tasks_file):
    id1 = task_manager.add_task("Task todo")
    id2 = task_manager.add_task("Task in progress")
    id3 = task_manager.add_task("Task done")
    task_manager.mark_task_in_progress(id2)
    task_manager.mark_task_done(id3)

    todos = task_manager.list_all_tasks_filtered(task_manager.TaskStatus.TODO)
    in_progress = task_manager.list_all_tasks_filtered(task_manager.TaskStatus.IN_PROGRESS)
    done = task_manager.list_all_tasks_filtered(task_manager.TaskStatus.DONE)

    assert len(todos) == 1 and todos[0]["id"] == id1
    assert len(in_progress) == 1 and in_progress[0]["id"] == id2
    assert len(done) == 1 and done[0]["id"] == id3

def test_update_task_not_found(temp_tasks_file):
    with pytest.raises(ValueError):
        task_manager.update_task(9999, "Doesn't exist")

def test_mark_task_done_not_found(temp_tasks_file):
    with pytest.raises(ValueError):
        task_manager.mark_task_done(8888)

def test_mark_task_in_progress_not_found(temp_tasks_file):
    with pytest.raises(ValueError):
        task_manager.mark_task_in_progress(7777)

def test_delete_task_not_found(temp_tasks_file):
    # delete_task zwraca False jeśli nie znajdzie, ale w Twojej implementacji rzuca wyjątek
    with pytest.raises(ValueError):
        task_manager.delete_task(6666)