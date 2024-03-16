import uvicorn

from decouple import config
from fastapi import FastAPI, Request, Response

import daiquiri

from application.commons.logging import configure as config_logging
from application.commons.response import make_response
from application.entrypoint import (
    categoria_controller,
    cliente_controller,
    pedido_controller,
    produto_controller,
    cognito_controller,
)
from infrastructure.database import init_db

HOST = config("HOST_API", default="localhost")
PORT = config("PORT_API", default="8000")

config_logging()

log = daiquiri.getLogger(__name__)

app = FastAPI(
    title="Foodie Flow",
    description="API - Tech Challenge - FIAP",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redocs",
)

app.router.redirect_slashes = True

app.include_router(cliente_controller.router, prefix="/clientes")
app.include_router(categoria_controller.router, prefix="/categorias")
app.include_router(produto_controller.router, prefix="/produtos")
app.include_router(pedido_controller.router, prefix="/pedidos")
app.include_router(cognito_controller.router, prefix="/cognito")


@app.on_event("startup")
async def startup_event():
    init_db()


@app.get("/healthcheck", description="Healthcheck da API")
@app.options("/healthcheck", description="Healthcheck da API")
async def healthcheck(request: Request) -> Response:
    log.info("Healthcheck solicitado")
    return make_response(request=request, body={"status": "UP"}, status_code=200)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=True,
        workers=1,
        server_header=False,
        access_log=False,
    )
