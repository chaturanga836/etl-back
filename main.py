from fastapi import FastAPI
from app.endpoints import root_router, items_router, etl_router
from app.db import Base, async_engine  # Import the asynchronous engine for table creation
from contextlib import asynccontextmanager

# Create tables using the asynchronous engine
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    # Add any cleanup code here if needed

app = FastAPI(lifespan=lifespan)

app.include_router(root_router, prefix="")
app.include_router(items_router, prefix="/items")
app.include_router(etl_router, prefix="/etl")

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.set_start_method("spawn")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
