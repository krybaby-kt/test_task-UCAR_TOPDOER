"""
Модуль для конфигурации FastAPI приложения.
"""
from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from web_api.endpoints.v1.incidents import router as incidents_router


app = FastAPI(
    title="Test Task UCAR TOPDOER",
    description="Backend API for Test Task UCAR TOPDOER",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

app.include_router(incidents_router, prefix="/api/v1/incidents", tags=["incidents"])


@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"], include_in_schema=False)
async def catch_all(request: Request, path_name: str):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
