from app.cruds.base import CRUDBase
from app.models.project import Project


class CRUDProject(CRUDBase[Project]):
    pass

project = CRUDProject(Project)