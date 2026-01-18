from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.db.engine import engine
from app.models import Base  # IMPORTANT: imports ALL models via __init__.py

# Alembic Config object
config = context.config

# Configure logging
fileConfig(config.config_file_name)

# THIS IS THE KEY LINE
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in offline mode."""
    context.configure(
        url=str(engine.url),
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in online mode."""
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
