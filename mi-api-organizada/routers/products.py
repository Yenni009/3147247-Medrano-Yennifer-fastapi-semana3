from fastapi import APIRouter, HTTPException
from typing import List
from models.product import ProductCreate, ProductUpdate, ProductResponse
from services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/", response_model=List[ProductResponse])
def get_products():
    return ProductService.get_all_products()

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    product = ProductService.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate):
    try:
        return ProductService.create_product(product)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate):
    updated_product = ProductService.update_product(product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return updated_product

@router.delete("/{product_id}")
def delete_product(product_id: int):
    deleted = ProductService.delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": f"Producto con ID {product_id} eliminado"}
