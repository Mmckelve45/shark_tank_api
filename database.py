import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL environment variable not set. "
        "Please set it to your PostgreSQL connection string. "
        "Example: postgresql://username:password@localhost/database_name"
    )

# Create engine with connection pooling and health checks
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
    echo=False           # Set to True for SQL debugging
)

# ----------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Note: For production deployments, consider using:
# - Connection pooling (pgbouncer)
# - Read/write replicas for scaling
# - SSL connections (sslmode=require in DATABASE_URL)
