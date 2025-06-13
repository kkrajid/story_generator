import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class Config:
    """Application configuration"""
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME", "postgres")
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    @classmethod
    def validate_config(cls):
        """Validate required configuration"""
        missing_vars = []
        if not cls.DB_PASS:
            missing_vars.append("DB_PASS")
        if not cls.DB_HOST:
            missing_vars.append("DB_HOST")
        if not cls.GEMINI_API_KEY:
            missing_vars.append("GEMINI_API_KEY")
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")