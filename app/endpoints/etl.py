from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import httpx
from app.models import Endpoint  # Ensure correct import
from app.db import get_db

router = APIRouter()

@router.post("/add_endpoint")
async def add_endpoint(name: str, url: str, db: Session = Depends(get_db)):
    endpoint = Endpoint(name=name, url=url)
    db.add(endpoint)
    db.commit()
    db.refresh(endpoint)
    return {"message": "Endpoint added", "endpoint": endpoint}

@router.post("/extract")
async def extract_data(name: str, db: Session = Depends(get_db)):
    endpoint = db.query(Endpoint).filter(Endpoint.name == name).first()
    if not endpoint:
        raise HTTPException(status_code=404, detail="Endpoint not found")

    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint.url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to extract data")

    extracted_data = response.json()
    return {"extracted_data": extracted_data, "message": "Data extracted"}

@router.post("/transform")
async def transform_data():
    # Your transformation logic here
    return {"message": "Data transformed"}

@router.post("/load")
async def load_data():
    # Your loading logic here
    return {"message": "Data loaded"}
