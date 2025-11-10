"""
Модуль для конфигурации схем для эндпоинтов для инцидентов.
"""
from pydantic import BaseModel, Field, ConfigDict
from database.enums import IncidentStatusEnum, IncidentSourceEnum
from datetime import datetime


class IncidentBaseResponse(BaseModel):
    """
    Схема для базового ответа на эндпоинты для инцидентов.
    """
    model_config = ConfigDict(use_enum_values=True)
    
    id: int = Field(..., description="ID of the incident")
    status: IncidentStatusEnum = Field(..., description="Status of the incident")
    source: IncidentSourceEnum = Field(..., description="Source of the incident")
    description: str = Field(..., description="Description of the incident", min_length=1, max_length=255)
    creating_date: datetime = Field(..., description="Creating date of the incident")


class IncidentCreateRequest(BaseModel):
    """
    Схема для запроса на создание инцидента.
    """
    model_config = ConfigDict(use_enum_values=True)
    
    status: IncidentStatusEnum = Field(..., description="Status of the incident")
    source: IncidentSourceEnum = Field(..., description="Source of the incident")
    description: str = Field(..., description="Description of the incident", min_length=1, max_length=255)


class IncidentCreateResponse(IncidentBaseResponse):
    """
    Схема для ответа на создание инцидента.
    """
    model_config = ConfigDict(use_enum_values=True)
    
    pass


class IncidentGetResponse(IncidentBaseResponse):
    """
    Схема для ответа на получение инцидента.
    """
    model_config = ConfigDict(use_enum_values=True)
    
    pass


class IncidentGetAllResponse(BaseModel):
    """
    Схема для ответа на получение всех инцидентов.
    """
    model_config = ConfigDict(use_enum_values=True)
    
    incidents: list[IncidentBaseResponse] = Field(..., description="List of incidents")


class IncidentUpdateRequest(BaseModel):
    """
    Схема для запроса на обновление инцидента.
    """
    model_config = ConfigDict(use_enum_values=True)

    status: IncidentStatusEnum | None = Field(None, description="Status of the incident")
    source: IncidentSourceEnum | None = Field(None, description="Source of the incident")
    description: str | None = Field(None, description="Description of the incident", min_length=1, max_length=255)


class IncidentUpdateResponse(IncidentBaseResponse):
    """
    Схема для ответа на обновление инцидента.
    """
    model_config = ConfigDict(use_enum_values=True)
    
    pass


__all__ = [
    "IncidentBaseResponse",
    "IncidentCreateRequest",
    "IncidentCreateResponse",
    "IncidentGetResponse",
    "IncidentGetAllResponse",
    "IncidentUpdateRequest",
    "IncidentUpdateResponse",
]
