from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.repositories.connection_repository import ConnectionRepository
from app.schemas.connection import ConnectionCreate

router = APIRouter(prefix="/connections", tags=["Connections"])

@router.post("/")
def create_connection(connection: ConnectionCreate, db: Session = Depends(get_db)):
    return ConnectionRepository.create_connection(db, connection)

@router.get("/")
def get_connections(db: Session = Depends(get_db)):
    return ConnectionRepository.get_all_connections(db)
