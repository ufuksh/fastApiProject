from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Modellerden MetaData'yı alın
from app.models.models import Base  # Doğru modül yolunu kontrol edin

# Alembic Config nesnesi
config = context.config

# Loglama yapılandırması
fileConfig(config.config_file_name)

# MetaData nesnesi
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
