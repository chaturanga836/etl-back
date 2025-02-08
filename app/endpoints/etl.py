from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.services.etl_service import ETLService

router = APIRouter()

class EndpointRequest(BaseModel):
    name: str
    path: str
    method: str
    query_params: dict = None
    body_params: dict = None
    base_url: str

class ExtractRequest(BaseModel):
    name: str

class ExtractResponse(BaseModel):
    extracted_data: dict
    message: str

class TransformResponse(BaseModel):
    message: str

class LoadResponse(BaseModel):
    message: str

@router.post("/add_endpoint")
async def add_endpoint(request: EndpointRequest, db: AsyncSession = Depends(get_db)):
    endpoint = await ETLService.add_endpoint(db, request.name, request.path, request.method, request.query_params, request.body_params, request.base_url)
    return {"message": "Endpoint added", "endpoint": endpoint}

@router.post("/extract", response_model=ExtractResponse)
async def extract_data(request: ExtractRequest, db: AsyncSession = Depends(get_db)):
    extracted_data = await ETLService.extract_data(db, request.name)
    return {"extracted_data": extracted_data, "message": "Data extracted"}

@router.post("/transform", response_model=TransformResponse)
async def transform_data():
    # Add your transformation logic here
    return {"message": "Data transformed"}

@router.post("/load", response_model=LoadResponse)
async def load_data():
    # Add your loading logic here
    return {"message": "Data loaded"}
