from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine
from app.db.connection import engine, Base
import asyncio

from contextlib import asynccontextmanager

# Importa o roteador principal do seu pacote 'router'
from app.api.router.routes import router as main_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    #[Inicia]
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    #[Fecha]
    await engine.dispose()

def create_app():
    app = FastAPI(lifespan=lifespan)

    '''
    configurações extras comentadas
    '''

    # origins = [
    #     # Adicione os domínios do seu front-end aqui
    # ]

    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=origins,
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    # )

    app.include_router(main_router, prefix="/api/v1")

    @app.get("/")
    async def read_root():
        return {"message": "API de Produtos está funcionando!"}

    return app

app = create_app()