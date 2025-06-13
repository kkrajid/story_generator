import logging
import google.generativeai as genai
from config import Config
from exceptions import StoryGenerationError

logger = logging.getLogger(__name__)

# Initialize Gemini AI
try:
    genai.configure(api_key=Config.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    logger.info("Gemini AI configured successfully")
except Exception as e:
    logger.error(f"Failed to configure Gemini AI: {e}")
    raise

# Story generation service
class StoryService:
    """Service class for story generation"""
    
    @staticmethod
    def create_story_prompt(character_name: str, character_details: str) -> str:
        """Create a simple but effective prompt for story generation"""
        return f"""
You are a great storyteller. Write an interesting short story about this character:

**Character Name:** {character_name}
**About the Character:** {character_details}

**What to include in your story:**

**Story Length:** Write about 1000-1200 words

**Story Parts:**
1. **Beginning:** Show us who the character is and where they are
2. **Problem:** Give the character something challenging to deal with
3. **Middle:** Show how the character tries to solve the problem
4. **Ending:** Show how things work out and what the character learns

**Make it interesting by:**
• Show the character's personality through what they do and say
• Use lots of details so we can picture everything clearly
• Include conversations between characters
• Make us care about what happens to the character
• Create some tension or excitement
• Give the character real emotions and feelings

**Writing tips:**
• Use simple, clear language
• Make each scene move the story forward
• Show us things instead of just telling us
• Make the character feel like a real person
• Include some surprises but make them make sense
• End the story in a way that feels complete

**What your story should feel like:**
• Engaging and easy to read
• Suitable for anyone to enjoy
• Focused on the character's journey
• Emotionally satisfying

Write the complete story now. Make sure it has a clear beginning, middle, and end:
"""
    
    @staticmethod
    def create_genre_prompt(character_name: str, character_details: str, story_type: str) -> str:
        """Create simple prompts for different types of stories"""
        base_prompt = f"""
You are a great storyteller. Write a {story_type} story about this character:

**Character Name:** {character_name}
**About the Character:** {character_details}

**Story Length:** About 1000-1200 words
"""
        
        if story_type == "mystery":
            extra_tips = """
**Mystery Story Tips:**
• Include a puzzle or mystery to solve
• Give clues throughout the story
• Make the reader want to figure it out
• Have a satisfying solution at the end
• Keep the reader guessing
"""
        elif story_type == "adventure":
            extra_tips = """
**Adventure Story Tips:**
• Include exciting action and challenges
• Take the character to interesting places
• Add some danger or risk
• Show the character being brave
• Make it fast-paced and thrilling
"""
        elif story_type == "funny":
            extra_tips = """
**Funny Story Tips:**
• Include humor and funny situations
• Make the character do amusing things
• Add funny dialogue and conversations
• Create silly or unexpected moments
• Keep it light-hearted and entertaining
"""
        elif story_type == "heartwarming":
            extra_tips = """
**Heartwarming Story Tips:**
• Focus on emotions and relationships
• Show kindness and caring
• Include touching or meaningful moments
• Make the reader feel good
• End with hope or happiness
"""
        else:
            extra_tips = """
**General Story Tips:**
• Make it interesting and engaging
• Focus on the character's growth
• Include realistic emotions
• Create a satisfying ending
"""
        
        return base_prompt + extra_tips + """

**Basic Story Structure:**
1. Start by showing us the character
2. Give them a problem or challenge
3. Show how they handle it
4. End with a resolution

Write the complete story now using simple, clear language:
"""
    
    @staticmethod
    async def generate_story(character_name: str, character_details: str, story_type: str = "general") -> str:
        """Generate a story using simple prompts"""
        try:
            if story_type != "general":
                prompt = StoryService.create_genre_prompt(character_name, character_details, story_type)
            else:
                prompt = StoryService.create_story_prompt(character_name, character_details)
            
            logger.info(f"Generating {story_type} story for character: {character_name}")
            
            # Simple generation settings
            generation_config = genai.types.GenerationConfig(
                temperature=0.7,  # Creative but not too random
                max_output_tokens=1500,  # Enough for a good story
            )
            
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            if not response.text:
                raise StoryGenerationError("No story was created")
            
            # Check if story is long enough
            word_count = len(response.text.split())
            if word_count < 300:
                logger.warning(f"Story is quite short: {word_count} words")
            
            logger.info(f"Story created successfully for {character_name} ({word_count} words)")
            return response.text
            
        except Exception as e:
            logger.error(f"Could not create story for {character_name}: {str(e)}")
            raise StoryGenerationError(f"Failed to create story: {str(e)}")
    
    @staticmethod
    async def improve_story(character_name: str, character_details: str, 
                           old_story: str, what_to_fix: str) -> str:
        """Make a story better based on feedback"""
        try:
            improve_prompt = f"""
Here is a story that needs to be improved:

**Character:** {character_name}
**Character Details:** {character_details}

**Current Story:**
{old_story}

**What needs to be better:**
{what_to_fix}

Please rewrite the story to fix these issues. Keep the same character and main idea, but make the improvements requested. Use simple, clear language and make sure the story is complete and interesting.

Write the improved story now:
"""
            
            logger.info(f"Improving story for character: {character_name}")
            
            response = model.generate_content(improve_prompt)
            
            if not response.text:
                raise StoryGenerationError("Could not improve the story")
            
            logger.info(f"Story improved successfully for character: {character_name}")
            return response.text
            
        except Exception as e:
            logger.error(f"Could not improve story for {character_name}: {str(e)}")
            raise StoryGenerationError(f"Failed to improve story: {str(e)}")