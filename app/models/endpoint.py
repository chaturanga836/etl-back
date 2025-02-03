from sqlalchemy import Column, Integer, String
from app.db import Base  # Import Base from db.py

class Endpoint(Base):
    __tablename__ = "endpoints"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    url = Column(String, unique=True, nullable=False)
