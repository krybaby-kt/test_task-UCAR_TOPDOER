from pydantic import BaseModel, Field, ConfigDict
from database.enums import IncidentStatusEnum, IncidentSourceEnum
from datetime import datetime


class IncidentCreateRequest(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    status: IncidentStatusEnum = Field(..., description="Status of the incident")
    source: IncidentSourceEnum = Field(..., description="Source of the incident")
    description: str = Field(..., description="Description of the incident", min_length=1, max_length=255)


class IncidentCreateResponse(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    id: int = Field(..., description="ID of the incident")
    status: IncidentStatusEnum = Field(..., description="Status of the incident")
    source: IncidentSourceEnum = Field(..., description="Source of the incident")
    description: str = Field(..., description="Description of the incident", min_length=1, max_length=255)
    creating_date: datetime = Field(..., description="Creating date of the incident")


class IncidentGetResponse(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    id: int = Field(..., description="ID of the incident")
    status: IncidentStatusEnum = Field(..., description="Status of the incident")
    source: IncidentSourceEnum = Field(..., description="Source of the incident")
    description: str = Field(..., description="Description of the incident", min_length=1, max_length=255)
    creating_date: datetime = Field(..., description="Creating date of the incident")


class IncidentGetAllResponse(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    incidents: list[IncidentGetResponse] = Field(..., description="List of incidents")


class IncidentUpdateRequest(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    status: IncidentStatusEnum | None = Field(None, description="Status of the incident")
    source: IncidentSourceEnum | None = Field(None, description="Source of the incident")
    description: str | None = Field(None, description="Description of the incident", min_length=1, max_length=255)


class IncidentUpdateResponse(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    id: int = Field(..., description="ID of the incident")
    status: IncidentStatusEnum = Field(..., description="Status of the incident")
    source: IncidentSourceEnum = Field(..., description="Source of the incident")
    description: str = Field(..., description="Description of the incident", min_length=1, max_length=255)
    creating_date: datetime = Field(..., description="Creating date of the incident")


__all__ = [
    "IncidentCreateRequest",
    "IncidentCreateResponse",
    "IncidentGetResponse",
    "IncidentGetAllResponse",
    "IncidentUpdateRequest",
    "IncidentUpdateResponse",
]
