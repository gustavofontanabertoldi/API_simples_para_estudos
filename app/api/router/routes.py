from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from app.db.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.DTOs.userDTO import UserDTO
from app.schemas.DTOs.productDTO import ProductDTO
from app.services.product import get_product_by_name, delete_product_by_name
from app.services.product import create_product as create_product_service
from fastapi.security import OAuth2PasswordBearer
from app.services.user import get_current_user, register_user

router = APIRouter()

#------------------PRODUCT--------------------

@router.get('/product/{name}')
async def get_product_name(name:str, db:AsyncSession = Depends(get_db)):
    result = await get_product_by_name(db=db, name=name)
    if not result:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    return result

@router.post('/product/create')
async def create_product(new_product:ProductDTO, db:AsyncSession = Depends(get_db)):
    created_product = await create_product_service(db=db, new_product=new_product)
    return created_product

@router.delete('/product/delete/{name}')
async def delete_product(name:str, db:AsyncSession = Depends(get_db)):
    await delete_product_by_name(db=db, name=name)
    return {"message": f"Produto '{name}' deletado com sucesso"}

#-------------------USER-----------------------

@router.post("/register")
async def add_user(new_user:UserDTO, db:AsyncSession=Depends(get_db)):
    created_user = await register_user(db=db, new_user=new_user)
    return created_user