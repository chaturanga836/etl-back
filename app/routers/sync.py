from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.sync_service import sync_data

router = APIRouter(prefix="/sync", tags=["Sync"])

@router.post("/")
async def sync_endpoint(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(sync_data, db)
    return {"message": "Data sync started in the background"}
