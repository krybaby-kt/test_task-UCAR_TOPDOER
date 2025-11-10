from database.base_repository import AsyncBaseIdSQLAlchemyCRUD
from asyncio import Lock

from database.models.incidents import IncidentModel


class IncidentRepository(AsyncBaseIdSQLAlchemyCRUD):
    model = IncidentModel
    field_id = "id"
    lock: Lock = Lock()
