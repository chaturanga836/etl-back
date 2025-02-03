from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context
from app.models import Base  # Import Base from models

# Alembic Config object
config = context.config

# Set up loggers
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Use combined metadata
target_metadata = Base.metadata

def get_url():
    return config.get_main_option("sqlalchemy.url")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(
        get_url(),
        poolclass=pool.NullPool,
    )

    async def async_main():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    import asyncio
    asyncio.run(async_main())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
