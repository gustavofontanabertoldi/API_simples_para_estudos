from fastapi import Depends
from app.db.connection import get_db
from app.schemas.DTOs.userDTO import UserDTO
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.Models.user_model import User
from sqlalchemy import select
from fastapi import Depends, HTTPException
from app.core.auth import oauth2_scheme, SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from app.core.auth import hash_password



async def get_current_user(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="invalid token")

async def get_user_by_name(username:str, db:AsyncSession = Depends(get_db), current_user:str = Depends(get_current_user)):
    result = await db.execute(select(User).where(User.username == username))
    _user = result.scalar_one_or_none()
    return _user

async def register_user(new_user:UserDTO, db:AsyncSession = Depends(get_db)):
    hashed_password = hash_password(new_user.password)
    _user = User(username = new_user.username, password = hashed_password)
    db.add(_user)
    await db.commit()
    await db.refresh(_user)
    return _user

async def update_user(
        username:str,
        updated_user:UserDTO,
        db:AsyncSession = Depends(get_db),
        current_user:str = Depends(get_current_user)
):
    if username != current_user:
        raise HTTPException(status_code=403, detail="access not permited")
    result = await db.execute(select(User).where(User.username == username))
    _user = result.scalar_one_or_none()
    if _user is None:
        raise HTTPException(status_code=401, detail="user not found")
    
    _user.username = updated_user.username
    _user.password = updated_user.password
    await db.commit()
    return {"msg", "user updated successfully"}

async def delete_user(
        username:str,
        db:AsyncSession = Depends(get_db),
        current_user:str = Depends(get_current_user)
):
    if username != current_user:
        raise HTTPException(status_code=403, detail="access not permited")
    result = await db.execute(select(User).where(User.username == username))
    _user = result.scalar_one_or_none()
    if _user is None:
        raise HTTPException(status_code=401, detail="user not found")
    db.delete(_user)
    await db.commit()
    return {"msg":"user deleted successfully"} 