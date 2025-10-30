from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

def register_error_handlers(app: FastAPI):
    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        return JSONResponse(
            status_code=400,
            content={
                "error": "Error de integridad en la base de datos",
                "detail": str(exc.orig),
                "type": "database_integrity_error"
            }
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "error": "Error de validación",
                "detail": exc.errors(),
                "type": "validation_error"
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Error interno del servidor",
                "detail": str(exc),
                "type": "internal_server_error"
            }
        )