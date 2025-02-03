from sqlalchemy import Column, String
from app.models import Base

class DataSource(Base):
    __tablename__ = 'data_source'
    
    name = Column(String, nullable=False)
    image = Column(String, nullable=True)
    description = Column(String, nullable=True)
    endpoint = Column(String, nullable=True)
