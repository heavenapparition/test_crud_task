import pytest

from app.cruds.project import CRUDProject
from app.database import Session
from app.models.project import Project


@pytest.fixture
def db():
    session = Session()
    try:
        yield session
    finally:
        session.close()

def test_create_project(session: Session):
    project_data = {"name": "Test Project", "description": "Test project description"}
    project = CRUDProject(Project).create(session=session, obj_in=project_data)
    assert project.name == project_data["name"]
    assert project.description == project_data["description"]

def test_get_project(session: Session):
    project_data = {"name": "Test Project", "description": "Test project description"}
    project = CRUDProject(Project).create(session=session, obj_in=project_data)
    session.commit()
    retrieved_project = CRUDProject(Project).get_one_by_id(session=session, id=project.id)
    assert retrieved_project.name == project_data["name"]
    assert retrieved_project.description == project_data["description"]

def test_update_project(session: Session):
    project_data = {"name": "Test Project", "description": "Test project description"}
    project = CRUDProject(Project).create(session=session, obj_in=project_data)
    db.commit()
    updated_project_data = {"name": "Updated Test Project", "description": "Updated test project description"}
    CRUDProject(Project).update(session=session, obj_current=project, obj_new=updated_project_data)
    db.commit()
    retrieved_project = CRUDProject(Project).get_one_by_id(session=session, id=project.id)
    assert retrieved_project.name == updated_project_data["name"]
    assert retrieved_project.description == updated_project_data["description"]

def test_delete_project(session: Session):
    project_data = {"name": "Test Project", "description": "Test project description"}
    project = CRUDProject(Project).create(session=session, obj_in=project_data)
    db.commit()
    CRUDProject(Project).delete(dsession=session, id=project.id)
    db.commit()
    retrieved_project = CRUDProject(Project).get_one_by_id(session=session, id=project.id)
    assert retrieved_project is None
