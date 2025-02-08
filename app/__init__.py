from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
import pkgutil
import importlib

metadata = MetaData()
Base = declarative_base(metadata=metadata)

# Dynamically import all modules in the current package
for module_info in pkgutil.iter_modules(__path__):
    importlib.import_module(f"{__name__}.{module_info.name}")

__all__ = ['Base', 'metadata']
