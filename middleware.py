import uuid
import logging
from fastapi import Request, Response
from fastapi.responses import JSONResponse

from schemas import ErrorResponse
from exceptions import CharacterNotFoundError, StoryGenerationError, DatabaseError

logger = logging.getLogger(__name__)

# Request ID middleware
async def request_id_middleware(request: Request, call_next):
    """Add request ID to each request for tracking"""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    logger.info(f"Request {request_id}: {request.method} {request.url}")
    
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    
    logger.info(f"Request {request_id} completed with status {response.status_code}")
    return response

# Exception handlers
async def character_not_found_handler(request: Request, exc: CharacterNotFoundError):
    logger.warning(f"Character not found: {str(exc)}")
    return JSONResponse(
        status_code=404,
        content=ErrorResponse(
            error="Character not found",
            detail=str(exc),
            timestamp=str(uuid.uuid4()),
            request_id=str(getattr(request.state, 'request_id', uuid.uuid4()))
        ).dict()
    )

async def story_generation_error_handler(request: Request, exc: StoryGenerationError):
    logger.error(f"Story generation error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Story generation failed",
            detail=str(exc),
            timestamp=str(uuid.uuid4()),
            request_id=str(getattr(request.state, 'request_id', uuid.uuid4()))
        ).dict()
    )

async def database_error_handler(request: Request, exc: DatabaseError):
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Database operation failed",
            detail=str(exc),
            timestamp=str(uuid.uuid4()),
            request_id=str(getattr(request.state, 'request_id', uuid.uuid4()))
        ).dict()
    )

async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail="An unexpected error occurred",
            timestamp=str(uuid.uuid4()),
            request_id=str(getattr(request.state, 'request_id', uuid.uuid4()))
        ).dict()
    )