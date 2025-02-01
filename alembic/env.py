from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from app.models import Base

# @ The configuration object is obtained from Alembic's context. This config will contain settings like the database URL.
config = context.config

# @ If the config file exists, it loads logging configurations from the file to set up logging behavior.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# @ The target_metadata is the metadata for the database schema, which will be used by Alembic for migrations.
target_metadata = Base.metadata

# @ Function to run migrations in offline mode, where the database connection URL is passed directly as a string.
def run_migrations_offline() -> None:
    # @ Get the URL for the database connection from the Alembic configuration.
    url = config.get_main_option("sqlalchemy.url")
    
    # @ Configure the migration context to use the provided URL and metadata.
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,  # @ Ensures that the SQL is generated with literal values instead of bound parameters.
        dialect_opts={"paramstyle": "named"},  # @ Sets the parameter style to 'named' for the SQL dialect.
    )

    # @ Begin a migration transaction and run migrations offline.
    with context.begin_transaction():
        context.run_migrations()

# @ Function to run migrations in online mode, where the connection to the database is managed via SQLAlchemy engine.
def run_migrations_online() -> None:
    # @ Create an SQLAlchemy engine from the configuration, with connection pooling options.
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # @ No connection pooling is used here.
    )

    # @ Establish a connection to the database and configure the migration context.
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        # @ Begin a migration transaction and run migrations online.
        with context.begin_transaction():
            context.run_migrations()

# @ Check whether Alembic is running in offline or online mode and call the respective function.
if context.is_offline_mode():
    run_migrations_offline()  # @ Run migrations offline if in offline mode.
else:
    run_migrations_online()  # @ Run migrations online if in online mode.
