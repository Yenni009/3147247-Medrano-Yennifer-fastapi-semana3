from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List
from datetime import datetime

class Book(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    author: str = Field(..., min_length=2, max_length=100)
    isbn: str = Field(..., pattern=r"^97[89]-\d{10}$")
    year: int = Field(..., ge=1500, le=datetime.now().year)
    rating: float = Field(..., ge=0, le=5)
    price: float = Field(..., gt=0)
    tags: List[str] = []
    is_available: bool = Field(default=True)
    is_bestseller: bool = Field(default=False)

    # Normaliza título con mayúsculas iniciales
    @field_validator("title")
    def validate_title(cls, v: str):
        return v.title()

    # Valida autor para que no sean solo números
    @field_validator("author")
    def validate_author(cls, v: str):
        if v.isnumeric():
            raise ValueError("El autor no puede ser solo números")
        return v

    # Evita tags duplicados
    @field_validator("tags")
    def validate_tags(cls, v: List[str]):
        if len(v) != len(set(v)):
            raise ValueError("Los tags no pueden estar duplicados")
        return v

    # Validaciones cruzadas
    @model_validator(mode="after")
    def validate_cross_fields(self):
        if self.is_bestseller and self.rating < 4.0:
            raise ValueError("Los bestsellers deben tener rating >= 4.0")
        if self.year < 1900:
            self.price = 10.0  # precio especial
        return self

