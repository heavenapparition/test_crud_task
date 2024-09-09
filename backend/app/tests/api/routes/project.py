from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.utils import random_lower_string, random_project_name


def test_create_project(client: TestClient, db: Session) -> None:
    project_name = random_project_name()
    project_description = random_lower_string()
    response = client.post(
        f"{settings.API_V1_STR}/projects/",
        json={"name": project_name, "description": project_description},
    )
    assert response.status_code == 201
    content = response.json()
    assert content["name"] == project_name
    assert content["description"] == project_description


def test_get_project(client: TestClient, db: Session) -> None:
    project_name = random_project_name()
    project_description = random_lower_string()
    response = client.post(
        f"{settings.API_V1_STR}/projects/",
        json={"name": project_name, "description": project_description},
    )
    project_id = response.json()["id"]
    response = client.get(f"{settings.API_V1_STR}/projects/{project_id}")
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == project_name
    assert content["description"] == project_description


def test_update_project(client: TestClient, db: Session) -> None:
    project_name = random_project_name()
    project_description = random_lower_string()
    response = client.post(
        f"{settings.API_V1_STR}/projects/",
        json={"name": project_name, "description": project_description},
    )
    project_id = response.json()["id"]
    new_project_name = random_project_name()
    new_project_description = random_lower_string()
    response = client.put(
        f"{settings.API_V1_STR}/projects/{project_id}",
        json={"name": new_project_name, "description": new_project_description},
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == new_project_name
    assert content["description"] == new_project_description


def test_delete_project(client: TestClient, db: Session) -> None:
    project_name = random_project_name()
    project_description = random_lower_string()
    response = client.post(
        f"{settings.API_V1_STR}/projects/",
        json={"name": project_name, "description": project_description},
    )
    project_id = response.json()["id"]
    response = client.delete(f"{settings.API_V1_STR}/projects/{project_id}")
    assert response.status_code == 200
    response = client.get(f"{settings.API_V1_STR}/projects/{project_id}")
    assert response.status_code == 404
