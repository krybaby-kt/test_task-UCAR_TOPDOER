from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware


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


@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"], include_in_schema=False)
async def catch_all(request: Request, path_name: str):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")