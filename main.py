from fastapi import FastAPI
from app.endpoints import root_router, items_router, etl_router
from app.db import Base, sync_engine  # Import synchronous engine for table creation

# Create tables using synchronous engine
Base.metadata.create_all(bind=sync_engine)

app = FastAPI()

app.include_router(root_router, prefix="")
app.include_router(items_router, prefix="/items")
app.include_router(etl_router, prefix="/etl")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
