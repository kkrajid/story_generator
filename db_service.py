import uuid
import logging
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from models import Character
from schemas import CharacterCreate
from exceptions import CharacterNotFoundError, DatabaseError

logger = logging.getLogger(__name__)

# Database service
class DatabaseService:
    """Service class for database operations"""
    
    @staticmethod
    async def create_character(db: AsyncSession, character_data: CharacterCreate) -> Character:
        """Create a new character in the database"""
        try:
            db_character = Character(name=character_data.name, details=character_data.details)
            db.add(db_character)
            await db.commit()
            await db.refresh(db_character)
            logger.info(f"Character created successfully: {db_character.id}")
            return db_character
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"Database error creating character: {str(e)}")
            raise DatabaseError(f"Failed to create character: {str(e)}")
    
    @staticmethod
    async def get_character_by_id(db: AsyncSession, character_id: uuid.UUID) -> Character:
        """Get a character by ID"""
        try:
            character = await db.get(Character, character_id)
            if not character:
                raise CharacterNotFoundError(f"Character with ID {character_id} not found")
            return character
        except SQLAlchemyError as e:
            logger.error(f"Database error getting character {character_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve character: {str(e)}")
    
    @staticmethod
    async def get_character_by_name(db: AsyncSession, character_name: str) -> Character:
        """Get a character by name"""
        try:
            result = await db.execute(select(Character).where(Character.name == character_name))
            character = result.scalar_one_or_none()
            if not character:
                raise CharacterNotFoundError(f"Character with name '{character_name}' not found")
            return character
        except SQLAlchemyError as e:
            logger.error(f"Database error getting character {character_name}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve character: {str(e)}")
    
    @staticmethod
    async def list_characters(db: AsyncSession) -> List[Character]:
        """List all characters"""
        try:
            result = await db.execute(select(Character))
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Database error listing characters: {str(e)}")
            raise DatabaseError(f"Failed to list characters: {str(e)}")