import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.models.task import Task, TaskCreate, TaskUpdate
from app.tests.utils.utils import random_lower_string


@pytest.fixture
def task() -> Task:
    return Task(title=random_lower_string(), description=random_lower_string())

def test_create_task(client: TestClient, session: Session, task: Task) -> None:
    task_data = TaskCreate(title=task.title, description=task.description)
    response = client.post(f"{settings.API_V1_STR}/tasks/", json=task_data.dict())
    assert response.status_code == 201
    created_task = response.json()
    assert created_task["title"] == task.title
    assert created_task["description"] == task.description

def test_update_task(client: TestClient, session: Session, task: Task) -> None:
    task_data = TaskCreate(title=task.title, description=task.description)
    response = client.post(f"{settings.API_V1_STR}/tasks/", json=task_data.dict())
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]
    updated_task_data = TaskUpdate(title=random_lower_string(), description=random_lower_string())
    response = client.put(f"{settings.API_V1_STR}/tasks/{task_id}", json=updated_task_data.dict())
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == updated_task_data.title
    assert updated_task["description"] == updated_task_data.description

def test_delete_task(client: TestClient, session: Session, task: Task) -> None:
    task_data = TaskCreate(title=task.title, description=task.description)
    response = client.post(f"{settings.API_V1_STR}/tasks/", json=task_data.dict())
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]
    response = client.delete(f"{settings.API_V1_STR}/tasks/{task_id}")
    assert response.status_code == 204

def test_get_task(client: TestClient, session: Session, task: Task) -> None:
    task_data = TaskCreate(title=task.title, description=task.description)
    response = client.post(f"{settings.API_V1_STR}/tasks/", json=task_data.dict())
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]
    response = client.get(f"{settings.API_V1_STR}/tasks/{task_id}")
    assert response.status_code == 200
    retrieved_task = response.json()
    assert retrieved_task["title"] == task.title
    assert retrieved_task["description"] == task.description

def test_get_tasks(client: TestClient, session: Session, task: Task) -> None:
    task_data = TaskCreate(title=task.title, description=task.description)
    response = client.post(f"{settings.API_V1_STR}/tasks/", json=task_data.dict())
    assert response.status_code == 201
    response = client.get(f"{settings.API_V1_STR}/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) > 0

#Фильтры
def test_get_tasks_due_date_filter(client: TestClient, session: Session, task: Task) -> None:
    # Создаем несколько задач с разными датами
    task1 = Task(title=random_lower_string(), description=random_lower_string(), due_date="2022-01-01")
    task2 = Task(title=random_lower_string(), description=random_lower_string(), due_date="2022-01-15")
    task3 = Task(title=random_lower_string(), description=random_lower_string(), due_date="2022-02-01")

    session.add(task1)
    session.add(task2)
    session.add(task3)
    session.commit()

    response = client.get(f"{settings.API_V1_STR}/tasks/?due_date_from=2022-01-10")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2

    response = client.get(f"{settings.API_V1_STR}/tasks/?due_date_to=2022-01-20")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2

    response = client.get(f"{settings.API_V1_STR}/tasks/?due_date_from=2022-01-10&due_date_to=2022-01-20")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1

def test_get_tasks_pagination(client: TestClient, session: Session, task: Task) -> None:
    for _ in range(10):
        task = Task(title=random_lower_string(), description=random_lower_string())
        session.add(task)
    session.commit()

    response = client.get(f"{settings.API_V1_STR}/tasks/?skip=0&limit=5")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 5

    response = client.get(f"{settings.API_V1_STR}/tasks/?skip=5&limit=5")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 5
