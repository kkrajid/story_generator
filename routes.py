import uuid
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, SessionLocal
from schemas import CharacterCreate, CharacterResponse, GenerateStoryRequest, StoryResponse
from db_service import DatabaseService
from ai_service import StoryService
from config import Config

logger = logging.getLogger(__name__)

# Create API router
router = APIRouter()

@router.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "message": "Character Story Generator API",
        "status": "healthy",
        "version": "2.0.0"
    }

@router.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check"""
    try:
        # Test database connection
        async with SessionLocal() as session:
            await session.execute(select(1))
        
        return {
            "status": "healthy",
            "database": "connected",
            "gemini_ai": "configured" if Config.GEMINI_API_KEY else "not_configured"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

@router.post("/characters/", response_model=CharacterResponse, tags=["Characters"])
async def create_character(
    character: CharacterCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Create a new character"""
    logger.info(f"Creating character: {character.name}")
    return await DatabaseService.create_character(db, character)

@router.get("/characters/{character_id}", response_model=CharacterResponse, tags=["Characters"])
async def get_character(
    character_id: uuid.UUID, 
    db: AsyncSession = Depends(get_db)
):
    """Get a character by ID"""
    logger.info(f"Retrieving character: {character_id}")
    return await DatabaseService.get_character_by_id(db, character_id)

@router.get("/characters/", response_model=List[CharacterResponse], tags=["Characters"])
async def list_characters(db: AsyncSession = Depends(get_db)):
    """List all characters"""
    logger.info("Listing all characters")
    return await DatabaseService.list_characters(db)

@router.post("/stories/generate/", response_model=StoryResponse, tags=["Stories"])
async def generate_story(
    request: GenerateStoryRequest, 
    db: AsyncSession = Depends(get_db)
):
    """Generate a story for a character"""
    logger.info(f"Generating story for character: {request.name}")
    
    # Get character from database
    character = await DatabaseService.get_character_by_name(db, request.name)
    
    # Generate story
    story = await StoryService.generate_story(character.name, character.details)
    
    # Calculate word count
    word_count = len(story.split())
    
    return StoryResponse(
        story=story,
        character_name=character.name,
        word_count=word_count
    )