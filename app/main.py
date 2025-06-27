from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine
from app.db.connection import engine, Base
import asyncio

# Importa o roteador principal do seu pacote 'router'
from app.api.router.routes import router as main_router

def create_app():
    app = FastAPI()

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

    @app.on_event("startup")
    async def startup_event():
        print('inicializing the aplication')
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @app.on_event("shutdown")
    async def shutdown_event():
        print("Desligando a aplicação...")
        await engine.dispose() # Fecha a conexão com o banco de dados
        print("Conexão com o banco de dados fechada.")

    app.include_router(main_router, prefix="/api/v1")

    @app.get("/")
    async def read_root():
        return {"message": "API de Produtos está funcionando!"}

    return app

app = create_app()