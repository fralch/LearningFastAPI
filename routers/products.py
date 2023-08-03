from fastapi import APIRouter

router = APIRouter( prefix="/products", tags=["products"]  )

products_list = [
    "product1",
    "product2",
    "product3",
    "product4"]

@router.get("/")
async def get_products():
    return products_list

@router.get("/{id}")
async def get_product(id: int):
    return products_list[id]