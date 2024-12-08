# alembic/env.py

from logging.config import fileConfig
import sys
import os
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Proje dizinini Python path'ine ekleyin
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Proje modüllerinizi içe aktarın
from app.database import Base  # SQLAlchemy Base sınıfınızı içe aktarın
from app.models import *      # Tüm modellerinizi içe aktarın

# Alembic config
config = context.config

# Log yapılandırmasını ayarla
fileConfig(config.config_file_name)

# MetaData'yı ayarla
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
