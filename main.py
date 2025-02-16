from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Import CORS Middleware
from app.routers.connections import router as connections_router
from app.routers.endpoints import router as endpoints_router
from app.db import Base, async_engine
from contextlib import asynccontextmanager

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, set specific domains for security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include Routers
app.include_router(connections_router, prefix="/api/connections")
app.include_router(endpoints_router, prefix="/api/endpoints")

@app.get("/")
def root():
    return {"message": "ETL API is running!"}

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.set_start_method("spawn")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
