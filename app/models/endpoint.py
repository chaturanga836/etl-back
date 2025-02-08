from sqlalchemy import Column, Integer, String, ForeignKey, JSON, text
from sqlalchemy.orm import relationship
from app.db import Base  # Import Base from db.py

class BaseURL(Base):
    __tablename__ = "base_urls"

    id = Column(Integer, primary_key=True, index=True)
    base_url = Column(String, unique=True, nullable=False)
    endpoints = relationship("Endpoint", back_populates="base_url", lazy='selectin')

class Endpoint(Base):
    __tablename__ = "endpoints"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    path = Column(String, nullable=False)
    method = Column(String, nullable=False, server_default=text("'GET'"))  # Default to GET
    query_params = Column(JSON, nullable=True)  # Store query parameters as a JSON object
    body_params = Column(JSON, nullable=True)  # Store body parameters as a JSON object
    base_url_id = Column(Integer, ForeignKey("base_urls.id"))
    base_url = relationship("BaseURL", back_populates="endpoints", lazy='selectin')

    def __init__(self, name, path, method="GET", query_params=None, body_params=None, base_url_id=None):
        self.name = name
        self.path = path
        self.method = method
        self.query_params = query_params or {}
        self.body_params = body_params or {}
        self.base_url_id = base_url_id
