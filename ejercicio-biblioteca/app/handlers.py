from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions import (
    BookNotFoundError,
    DuplicateISBNError,
    InvalidBookDataError,
    BookNotAvailableError,
    LibraryFullError,
)
from datetime import datetime

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(BookNotFoundError)
    async def book_not_found_handler(request: Request, exc: BookNotFoundError):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "error_code": "BOOK_NOT_FOUND",
                "message": str(exc),
                "timestamp": datetime.now().isoformat()
            },
        )

    @app.exception_handler(DuplicateISBNError)
    async def duplicate_isbn_handler(request: Request, exc: DuplicateISBNError):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error_code": "DUPLICATE_ISBN",
                "message": str(exc),
                "timestamp": datetime.now().isoformat()
            },
        )

    @app.exception_handler(InvalidBookDataError)
    async def invalid_data_handler(request: Request, exc: InvalidBookDataError):
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error_code": "INVALID_DATA",
                "message": str(exc),
                "timestamp": datetime.now().isoformat()
            },
        )

    @app.exception_handler(BookNotAvailableError)
    async def not_available_handler(request: Request, exc: BookNotAvailableError):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error_code": "NOT_AVAILABLE",
                "message": str(exc),
                "timestamp": datetime.now().isoformat()
            },
        )

    @app.exception_handler(LibraryFullError)
    async def library_full_handler(request: Request, exc: LibraryFullError):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error_code": "LIBRARY_FULL",
                "message": str(exc),
                "timestamp": datetime.now().isoformat()
            },
        )
