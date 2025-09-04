from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Optional
from datetime import datetime

class Book(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    author: str = Field(..., min_length=2, max_length=100)
    isbn: str = Field(..., regex=r"^97[89]-\d{10}$")
    year: int = Field(..., ge=1500, le=datetime.now().year)
    rating: float = Field(..., ge=0, le=5)
    price: float = Field(..., gt=0)
    tags: List[str] = []
    is_available: bool = Field(True)
    is_bestseller: bool = Field(False)

    @validator("title")
    def validate_title(cls, v):
        return v.title()

    @validator("author")
    def validate_author(cls, v):
        if v.isnumeric():
            raise ValueError("El autor no puede ser solo números")
        return v

    @validator("tags")
    def validate_tags(cls, v):
        if len(v) != len(set(v)):
            raise ValueError("Los tags no pueden estar duplicados")
        return v

    @root_validator
    def validate_cross_fields(cls, values):
        if values.get("is_bestseller") and values.get("rating", 0) < 4.0:
            raise ValueError("Los bestsellers deben tener rating >= 4.0")
        if values.get("year") < 1900:
            values["price"] = 10.0  # precio especial
        return values
