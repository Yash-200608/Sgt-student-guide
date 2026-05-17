import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError

from app.config.database import close_mongo_connection, connect_to_mongo
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.routes import (
    admin,
    analytics,
    attendance,
    auth,
    bus_routes,
    clubs,
    events,
    notices,
    notifications,
    personalization,
    search,
    teachers,
    timetable,
)
from app.utils.response import error_response, success_response

logger = logging.getLogger(__name__)

ALLOWED_ORIGINS = [
    "https://sgt-student-guide.vercel.app",
]


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    await connect_to_mongo()
    try:
        yield
    finally:
        await close_mongo_connection()


def _register_routes(application: FastAPI) -> None:
    application.include_router(auth.router)
    application.include_router(personalization.router)
    application.include_router(timetable.router)
    application.include_router(events.router)
    application.include_router(notices.router)
    application.include_router(teachers.router)
    application.include_router(clubs.router)
    application.include_router(notifications.router)
    application.include_router(attendance.router)
    application.include_router(bus_routes.router)
    application.include_router(search.router)
    application.include_router(admin.router)
    application.include_router(analytics.router)

    @application.get("/api/health", tags=["Health"])
    async def health_check() -> dict[str, Any]:
        return success_response("SGT Navigator API is running.", {"status": "ok"})


def _configure_cors(application: FastAPI) -> None:
    application.add_middleware(SecurityHeadersMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "https://sgt-student-guide.vercel.app"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def _register_exception_handlers(application: FastAPI) -> None:
    @application.exception_handler(HTTPException)
    async def http_exception_handler(
        _request: Request,
        exc: HTTPException,
    ) -> JSONResponse:
        message = exc.detail if isinstance(exc.detail, str) else "Request failed."
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(message),
        )

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        _request: Request,
        _exc: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=error_response("Validation failed. Please check the submitted data."),
        )

    @application.exception_handler(PyMongoError)
    async def database_exception_handler(
        _request: Request,
        exc: PyMongoError,
    ) -> JSONResponse:
        logger.exception("MongoDB operation failed: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=error_response("Database operation failed."),
        )

    @application.exception_handler(Exception)
    async def unhandled_exception_handler(
        _request: Request,
        exc: Exception,
    ) -> JSONResponse:
        logger.exception("Unhandled application error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response("Internal server error."),
        )


def create_app() -> FastAPI:
    application = FastAPI(
        title="SGT Navigator API",
        description="Backend APIs for the SGT Navigator university dashboard.",
        version="2.0.0",
        lifespan=lifespan,
    )
    _configure_cors(application)
    _register_exception_handlers(application)
    _register_routes(application)
    return application


app = create_app()
