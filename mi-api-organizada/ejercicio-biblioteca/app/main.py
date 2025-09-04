from fastapi import FastAPI
from app.models import Book
from app.exceptions import (
    BookNotFoundError,
    DuplicateISBNError,
    InvalidBookDataError,
    BookNotAvailableError,
    LibraryFullError,
)
from app.handlers import register_exception_handlers

app = FastAPI(
    title="Library Management API",
    version="1.0.0",
    description="API para gestión de libros, préstamos y categorías"
)

# Registrar manejadores de errores
register_exception_handlers(app)

# Base de datos simulada
books_db = []

# Endpoint de salud
@app.get("/health")
def health_check():
    return {"success": True, "message": "API funcionando correctamente"}
