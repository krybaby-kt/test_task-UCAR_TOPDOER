from fastapi import APIRouter, Request, Path, Query, Body
from fastapi import status as fastapi_status
from web_api.endpoints.v1.incidents.schematics import *
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from database.models.incidents import IncidentModel
from database.repositories.incidents import IncidentRepository
from utils.exception_handler.decorator import handle_async
from database.enums import IncidentStatusEnum, IncidentSourceEnum
from datetime import datetime


router = APIRouter()


@router.post(
    "/create",
    summary="Create incident",
    description="Create incident",
    response_model=IncidentCreateResponse,
    response_model_exclude_none=True,
    status_code=fastapi_status.HTTP_201_CREATED,
)
async def create_incident(
    request: Request,
    incident_create_request: IncidentCreateRequest,
):
    try:
        db_incident: IncidentModel = await IncidentRepository.create(data=dict(
            status=incident_create_request.status,
            source=incident_create_request.source,
            description=incident_create_request.description,
        ))

        return JSONResponse(
            status_code=fastapi_status.HTTP_201_CREATED,
            content=IncidentCreateResponse(
                id=db_incident.id,
                status=db_incident.status,
                source=db_incident.source,
                description=db_incident.description,
                creating_date=db_incident.creating_date,
            ).model_dump(mode='json'),
        )
    except HTTPException:
        raise
    except Exception as ex_:
        await handle_async(function_category="web_api", function="create_incident", exception=ex_)
        raise HTTPException(status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex_))


@router.get(
    "/get/{incident_id}",
    summary="Get incident by ID",
    description="Get incident by ID",
    response_model=IncidentGetResponse,
    response_model_exclude_none=True,
    status_code=fastapi_status.HTTP_200_OK,
)
async def get_incident(
    request: Request,
    incident_id: int = Path(..., description="ID of the incident"),
):
    try:
        db_incident: IncidentModel = await IncidentRepository(incident_id).get()
        if not db_incident:
            raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND, detail="Incident not found")
        
        return JSONResponse(
            status_code=fastapi_status.HTTP_200_OK,
            content=IncidentGetResponse(
                id=db_incident.id,
                status=db_incident.status,
                source=db_incident.source,
                description=db_incident.description,
                creating_date=db_incident.creating_date,
            ).model_dump(mode='json'),
        )
    except HTTPException:
        raise
    except Exception as ex_:
        await handle_async(function_category="web_api", function="get_incident", exception=ex_)
        raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND, detail="Incident not found")


@router.get(
    "/get",
    summary="Get all incidents with pagination",
    description="Get all incidents with pagination",
    response_model=IncidentGetAllResponse,
    response_model_exclude_none=True,
    status_code=fastapi_status.HTTP_200_OK,
)
async def get_all_incidents(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Page size"),
    incident_status: IncidentStatusEnum | None = Query(None, description="Status of the incident"),
    incident_source: IncidentSourceEnum | None = Query(None, description="Source of the incident"),
    creating_date_from: datetime | None = Query(None, description="Creating date from"),
    creating_date_to: datetime | None = Query(None, description="Creating date to"),
):
    try:
        filters = []
        if incident_status:
            filters.append(IncidentModel.status == incident_status)
        if incident_source:
            filters.append(IncidentModel.source == incident_source)
        if creating_date_from:
            filters.append(IncidentModel.creating_date >= creating_date_from)
        if creating_date_to:
            filters.append(IncidentModel.creating_date <= creating_date_to)

        db_incidents: list[IncidentModel] = await IncidentRepository.get_all_with_filters(filters=filters, limit=page_size, offset=(page - 1) * page_size, sort_by=IncidentModel.creating_date, sort_order="desc")
        
        return JSONResponse(
            status_code=fastapi_status.HTTP_200_OK,
            content=IncidentGetAllResponse(
                incidents=[IncidentGetResponse(
                    id=incident.id,
                    status=incident.status,
                    source=incident.source,
                    description=incident.description,
                    creating_date=incident.creating_date,
                ) for incident in db_incidents],
            ).model_dump(mode='json'),
        )
    except HTTPException:
        raise
    except Exception as ex_:
        await handle_async(function_category="web_api", function="get_all_incidents", exception=ex_)
        raise HTTPException(status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex_))


@router.put(
    "/update/{incident_id}",
    summary="Update incident by ID",
    description="Update incident by ID",
    response_model=IncidentUpdateResponse,
    response_model_exclude_none=True,
    status_code=fastapi_status.HTTP_200_OK,
)
async def update_incident(
    request: Request,
    incident_id: int = Path(..., description="ID of the incident"),
    incident_update_request: IncidentUpdateRequest = Body(..., description="Incident update request"),
):
    try:
        if not await IncidentRepository(incident_id).get():
            raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND, detail="Incident not found")
        
        await IncidentRepository(incident_id).update(data=dict(
            status=incident_update_request.status,
            source=incident_update_request.source,
            description=incident_update_request.description,
        ))
        db_incident: IncidentModel = await IncidentRepository(incident_id).get()
        
        return JSONResponse(
            status_code=fastapi_status.HTTP_200_OK,
            content=IncidentUpdateResponse(
                id=db_incident.id,  
                status=db_incident.status,
                source=db_incident.source,
                description=db_incident.description,
                creating_date=db_incident.creating_date,
            ).model_dump(mode='json'),
        )
    except HTTPException:
        raise
    except Exception as ex_:
        await handle_async(function_category="web_api", function="update_incident", exception=ex_)
        raise HTTPException(status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex_))
