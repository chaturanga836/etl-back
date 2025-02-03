from sqlalchemy import MetaData, Column, Integer, DateTime, SmallInteger
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from datetime import datetime, timezone

class BaseMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    status = Column(SmallInteger, server_default='0')

metadata = MetaData()
Base = declarative_base(metadata=metadata, cls=BaseMixin)
