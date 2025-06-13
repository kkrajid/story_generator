# Custom exceptions
class CharacterNotFoundError(Exception):
    """Raised when a character is not found"""
    pass

class StoryGenerationError(Exception):
    """Raised when story generation fails"""
    pass

class DatabaseError(Exception):
    """Raised when database operations fail"""
    pass