from sqlalchemy import Column, Integer, String, JSON, DateTime, Text, func
from app.db import Base  # Import Base from db.py

class ApiResponse(Base):
    __tablename__ = "api_responses"

    id = Column(Integer, primary_key=True, index=True)
    endpoint_name = Column(String, index=True, nullable=False)
    status_code = Column(Integer, nullable=False)  # Add status_code field
    headers = Column(JSON, nullable=False)  # Add headers field
    response_data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
