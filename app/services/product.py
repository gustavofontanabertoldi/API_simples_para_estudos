from fastapi import Depends
from app.db.connection import get_db
from app.schemas.DTOs.productDTO import ProductDTO
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.Models.product_model import Product
from sqlalchemy import select
from fastapi import Depends, HTTPException

async def create_product(new_product:ProductDTO, db:AsyncSession = Depends(get_db)):
    _product = Product(name = new_product.name, description = new_product.description)
    db.add(_product)
    await db.commit()
    await db.refresh(_product)
    return _product

async def get_product_by_name(name:str, db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.name == name))
    product = result.scalar_one_or_none()
    return product

async def delete_product_by_name(name:str, db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.name == name))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail='produto não encontrado')
    
    await db.delete(product)
    await db.commit()

    return True