from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from utils.deps import get_session
from routes.plant_routes import router as plant_router
from routes.environment_routes import router as environment_router
from routes.actuator_routes import router as actuator_router
from routes.user_routes import router as user_router
from routes.hydroponic_routes import router as hydroponic_router

import aiocoap
import aiocoap.resource as resource
from contextlib import asynccontextmanager
from routes.coap_handler import HydroponicCoAPResource
from utils.aggregator import aggregator
from utils.manager import manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up CoAP server...")

    root = resource.Site()

    root.add_resource(
        ["coap", "hydroponics", "sensor"],
        HydroponicCoAPResource(
            role="sensor",
            aggregator=aggregator,
            manager=manager,
        ),
    )
    root.add_resource(
        ["coap", "hydroponics", "environment"],
        HydroponicCoAPResource(
            role="environment",
            aggregator=aggregator,
            manager=manager,
        ),
    )
    root.add_resource(
        ["coap", "hydroponics", "actuator"],
        HydroponicCoAPResource(
            role="actuator",
            aggregator=aggregator,
            manager=manager,
        ),
    )

    coap_context = await aiocoap.Context.create_server_context(
        root, bind=("localhost", 5683)
    )

    yield

    print("Shutting down CoAP server...")
    await coap_context.shutdown()


app = FastAPI(
    title="Smart Hydroponic API",
    version="2.0.0",
    redoc_url=None,
    lifespan=lifespan,
)

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plant_router)
app.include_router(environment_router)
app.include_router(actuator_router)
app.include_router(user_router)
app.include_router(hydroponic_router)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/db-test")
async def db_test(session: AsyncSession = Depends(get_session)):
    result = await session.execute(text("SELECT 1"))
    return {"result": result.scalar()}
