from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db import Base 

class Connection(Base):
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    base_url = Column(String, nullable=False)
    headers = Column(JSON, nullable=True)  # Store headers as JSON
    auth_type = Column(String, nullable=True)  # e.g., "Bearer", "Basic"
    auth_token = Column(String, nullable=True)  # Store API token if needed

    endpoints = relationship("Endpoint", back_populates="connection", cascade="all, delete")

class Endpoint(Base):
    __tablename__ = "endpoints"

    id = Column(Integer, primary_key=True, index=True)
    connection_id = Column(Integer, ForeignKey("connections.id"), nullable=False)
    path = Column(String, nullable=False)  # Example: "/api/add"
    method = Column(String, nullable=False, default="GET")  # GET, POST, etc.
    query_params = Column(JSON, nullable=True)  # Store query params as JSON
    body_params = Column(JSON, nullable=True)  # Store request body as JSON

    connection = relationship("Connection", back_populates="endpoints")
