import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# .env dosyasını yükleyin
load_dotenv()

# Alembic Config nesnesi
config = context.config

# .env'den DATABASE_URL'i al ve Alembic'e tanımla
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Loglama yapılandırması
fileConfig(config.config_file_name)

# Modelleri ve MetaData'yı içe aktarın
from app.models import Base
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
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
