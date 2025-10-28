from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from utils.deps import get_session
from config.config import settings
from routes.plant_routes import router as plant_router
from routes.environment_routes import router as environment_router
from routes.actuator_routes import router as actuator_router
from routes.user_routes import router as user_router


app = FastAPI(title="Smart Hydroponic API", version="2.0.0")

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

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
      <head><title>Smart Hydroponic API</title></head>
      <body>
        <h1>Welcome to Smart Hydroponic API</h1>
        <p>Go to <a href="/docs">/docs</a> for API documentation.</p>
      </body>
    </html>
    """

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/db-test")
async def db_test(session: AsyncSession = Depends(get_session)):
    result = await session.execute(text("SELECT 1"))
    return {"result": result.scalar()}
