import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import Config, logger
from database import engine
from models import Base
from routes import router
from middleware import (
    request_id_middleware,
    character_not_found_handler,
    story_generation_error_handler,
    database_error_handler,
    general_exception_handler
)
from exceptions import CharacterNotFoundError, StoryGenerationError, DatabaseError

# Validate configuration on startup
try:
    Config.validate_config()
    logger.info("Configuration validation passed")
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    raise

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting application...")
    try:
        # Startup
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
        yield
    except Exception as e:
        logger.error(f"Application startup failed: {str(e)}")
        raise
    finally:
        # Shutdown
        logger.info("Shutting down application...")
        await engine.dispose()
        logger.info("Application shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="Character Story Generator API",
    description="An API for creating characters and generating stories about them",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Add request ID middleware
app.middleware("http")(request_id_middleware)

# Global exception handlers
app.add_exception_handler(CharacterNotFoundError, character_not_found_handler)
app.add_exception_handler(StoryGenerationError, story_generation_error_handler)
app.add_exception_handler(DatabaseError, database_error_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )