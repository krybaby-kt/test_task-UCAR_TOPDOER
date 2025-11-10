from database.base_model import SQLAlchemyModel
from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
from database.enums import IncidentStatusEnum


class IncidentModel(SQLAlchemyModel):
    __tablename__ = "incidents"
    id = Column(Integer, unique=True, primary_key=True)

    description = Column(String, nullable=False)
    status = Column(Enum(IncidentStatusEnum), nullable=False)
    source = Column(String, nullable=False)

    creating_date = Column(DateTime, nullable=False, default=datetime.now)
