import logging
from urllib.parse import quote_plus
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import Config

logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = f"postgresql+asyncpg://{Config.DB_USER}:{quote_plus(Config.DB_PASS)}@{Config.DB_HOST}:5432/{Config.DB_NAME}"
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,   # Recycle connections after 1 hour
    echo=False           # Set to True for SQL query logging
)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Database dependency
async def get_db():
    """Database session dependency"""
    async with SessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {str(e)}")
            await session.rollback()
            raise
        finally:
            await session.close()