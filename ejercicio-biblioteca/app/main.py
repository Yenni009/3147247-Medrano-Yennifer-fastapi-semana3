from fastapi import FastAPI, HTTPException
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


@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Biblioteca"}



@app.get("/health")
def health_check():
    return {"success": True, "message": "API funcionando correctamente"}



# Crear un libro
@app.post("/books", response_model=Book)
def create_book(book: Book):
    # Verificar si ya existe ISBN
    for b in books_db:
        if b.isbn == book.isbn:
            raise HTTPException(status_code=400, detail="El ISBN ya existe")
    books_db.append(book)
    return book


# Listar todos los libros
@app.get("/books", response_model=list[Book])
def list_books():
    return books_db


# Obtener un libro por ISBN
@app.get("/books/{isbn}", response_model=Book)
def get_book(isbn: str):
    for book in books_db:
        if book.isbn == isbn:
            return book
    raise HTTPException(status_code=404, detail="Libro no encontrado")


# Actualizar un libro
@app.put("/books/{isbn}", response_model=Book)
def update_book(isbn: str, updated_book: Book):
    for i, book in enumerate(books_db):
        if book.isbn == isbn:
            books_db[i] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Libro no encontrado")


# Eliminar un libro 
@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    for i, book in enumerate(books_db):
        if book.isbn == isbn:
            del books_db[i]
            return {"message": "Libro eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

