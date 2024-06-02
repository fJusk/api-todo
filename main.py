import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api import v1_router
from src.api.schemas import DefaultResponse
from src.core.config import ALLOWED_ORIGINS, config
from src.core.exceptions import RecordNotFoundError

logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


app = FastAPI(
    title="Todo API",
    version="1.0.0",
    description="API for managing todo tasks",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(v1_router)


@app.exception_handler(RecordNotFoundError)
async def record_not_found_exception_handler(_, exc: RecordNotFoundError):
    return JSONResponse(
        status_code=404,
        content=DefaultResponse(success=False, message=str(exc)).model_dump(),
    )
