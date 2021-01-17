import os
import uvicorn

from fastapi import FastAPI

from auth import controller as authController
from rota import controller as rotaController
from vendedor import controller as vendedorController
from cliente import controller as clienteController

app = FastAPI(title="Desafio Stone - RestAPI",  description="<h3>EndPoints referentes a aplicação</h3>")

app.include_router(authController.router)
app.include_router(rotaController.router)
app.include_router(vendedorController.router)
app.include_router(clienteController.router)