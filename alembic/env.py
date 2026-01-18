import os
import sys
from logging.config import fileConfig
from pathlib import Path # <--- NUEVO: Para rutas exactas

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# --- 1. CONFIGURACION DE RUTAS ---
# Calculamos la ruta raiz del proyecto (2 niveles arriba de este archivo)
BASE_DIR = Path(__file__).resolve().parent.parent

# Agregamos la raiz al PATH de Python para encontrar 'backend'
sys.path.insert(0, str(BASE_DIR))

# --- 2. CARGAR VARIABLES DE ENTORNO (FORZADO) ---
from dotenv import load_dotenv
env_path = BASE_DIR / ".env"
load_dotenv(env_path) # <--- Cargamos el archivo especifico

# --- 3. IMPORTAR MODELOS ---
from backend.main import Base

# Configuración de logging
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# --- 4. VALIDAR E INYECTAR URL ---
database_url = os.getenv("DATABASE_URL")

if not database_url:
    # Si falla esto, cortamos la ejecucion para que no use la URL default
    raise ValueError("ERROR CRITICO: Alembic no encontro DATABASE_URL en .env")

# Sobreescribimos la configuracion
config.set_main_option("sqlalchemy.url", database_url)

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()