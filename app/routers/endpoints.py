from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Endpoint, Connection
from app.schemas import EndpointCreate

router = APIRouter(prefix="/endpoints", tags=["Endpoints"])

@router.post("/{connection_id}/")
def create_endpoint(connection_id: int, endpoint: EndpointCreate, db: Session = Depends(get_db)):
    connection = db.query(Connection).filter(Connection.id == connection_id).first()
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    db_endpoint = Endpoint(**endpoint.dict(), connection_id=connection_id)
    db.add(db_endpoint)
    db.commit()
    db.refresh(db_endpoint)
    return db_endpoint

@router.get("/{connection_id}/")
def get_endpoints(connection_id: int, db: Session = Depends(get_db)):
    return db.query(Endpoint).filter(Endpoint.connection_id == connection_id).all()
