from sqlalchemy.orm import Session
from app.models.connection import Connection
from app.schemas.connection import ConnectionCreate

class ConnectionRepository:
    @staticmethod
    def create_connection(db: Session, connection_data: ConnectionCreate):
        db_connection = Connection(**connection_data.dict())
        db.add(db_connection)
        db.commit()
        db.refresh(db_connection)
        return db_connection

    @staticmethod
    def get_all_connections(db: Session):
        return db.query(Connection).all()
