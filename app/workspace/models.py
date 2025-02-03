from sqlalchemy import Column, String
from app.models import Base

class Workspace(Base):
    __tablename__ = 'workspace_template'

    workspace_table = Column(String, unique=True, index=True)
    description = Column(String, unique=True, index=True)
