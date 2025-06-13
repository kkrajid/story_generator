# Character Story Generator API

A FastAPI-based web service that creates characters and generates personalized stories about them using Google's Gemini AI.

## 🚀 Features

- **Character Management**: Create and store character profiles with detailed descriptions
- **AI Story Generation**: Generate engaging stories using Google's Gemini AI
- **Multiple Story Types**: Support for general, mystery, adventure, funny, and heartwarming stories
- **Story Improvement**: Enhance existing stories based on feedback
- **RESTful API**: Clean, documented API endpoints
- **Async Support**: Built with modern async/await patterns
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **Request Tracking**: Unique request IDs for debugging and monitoring
- **Comprehensive Error Handling**: Detailed error responses with proper HTTP status codes

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **AI Service**: Google Gemini AI (gemini-1.5-flash)
- **Database**: PostgreSQL with asyncpg
- **ORM**: SQLAlchemy (async)
- **Validation**: Pydantic
- **Environment**: Python 3.8+

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Google Gemini API key

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kkrajid/story_generator.git
   cd story_generator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   # Supabase Configuration
   SUPABASE_URL=your_project_url
   SUPABASE_KEY=your_project_api_key
   SUPABASE_DB_PASSWORD=your_database_password
   
   # Google Gemini AI
   GEMINI_API_KEY=your_gemini_api_key
   ```

5. **Set up Supabase**
   
   a. Create a Supabase account at [https://supabase.com](https://supabase.com)
   
   b. Create a new project in Supabase
   
   c. Get your Supabase credentials from the project settings:
      - Project URL
      - Project API Key (anon/public)
      - Database Password
   
   d. The database will be automatically created and configured in Supabase. No manual database creation is needed.

## 🚀 Running the Application

### Development Mode
```bash
python main.py
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 📚 API Endpoints

### Health Check
- `GET /` - Basic health check
- `GET /health` - Detailed health check with service status

### Characters
- `POST /characters/` - Create a new character
- `GET /characters/{character_id}` - Get character by ID
- `GET /characters/` - List all characters

### Stories
- `POST /stories/generate/` - Generate a story for a character

## 📖 Usage Examples

### Creating a Character
```bash
curl -X POST "http://localhost:8000/characters/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Wonder",
    "details": "A curious 12-year-old girl who loves exploring mysterious places and solving puzzles. She has bright blue eyes, golden hair, and always carries a small notebook to write down her discoveries."
  }'
```

### Generating a Story
```bash
curl -X POST "http://localhost:8000/stories/generate/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Wonder"
  }'
```

### Python Client Example
```python
import requests

# Create a character
character_data = {
    "name": "Detective Holmes",
    "details": "A brilliant detective with keen observation skills and logical reasoning abilities."
}

response = requests.post("http://localhost:8000/characters/", json=character_data)
character = response.json()

# Generate a story
story_request = {"name": "Detective Holmes"}
story_response = requests.post("http://localhost:8000/stories/generate/", json=story_request)
story = story_response.json()

print(f"Generated story ({story['word_count']} words):")
print(story['story'])
```

## 🗂️ Project Structure

```
character-story-generator/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration management
├── database.py          # Database connection and session management
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic models for request/response validation
├── routes.py            # API route definitions
├── db_service.py        # Database service layer
├── ai_service.py        # AI story generation service
├── middleware.py        # Custom middleware and exception handlers
├── exceptions.py        # Custom exception classes
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── app.log             # Application logs (auto-generated)
└── README.md           # This file
```

## 🎨 Story Types

The API supports different story types through the `story_type` parameter:

- **general** (default): Balanced story with character development
- **mystery**: Puzzle-solving adventures with clues and revelations
- **adventure**: Action-packed stories with exciting challenges
- **funny**: Humorous stories with comedic situations
- **heartwarming**: Emotional stories focusing on relationships and feelings

## 🔍 Error Handling

The API provides comprehensive error handling with detailed responses:

```json
{
  "error": "Character not found",
  "detail": "Character with name 'Unknown Character' not found",
  "timestamp": "2025-06-14T10:30:00Z",
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

Common HTTP status codes:
- `200` - Success
- `404` - Character not found
- `422` - Validation error
- `500` - Server error (database or AI service issues)
- `503` - Service unavailable

## 📊 Logging

The application logs important events and errors:
- Request/response tracking with unique request IDs
- Character creation and retrieval operations
- Story generation attempts and results
- Database connection issues
- AI service errors

Logs are written to both console and `app.log` file.

## 🔐 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SUPABASE_URL` | Supabase project URL | Yes | - |
| `SUPABASE_KEY` | Supabase project API key | Yes | - |
| `SUPABASE_DB_PASSWORD` | Supabase database password | Yes | - |
| `GEMINI_API_KEY` | Google Gemini API key | Yes | - |

## 🧪 Testing

### Manual Testing
Use the interactive API documentation at `/docs` to test endpoints manually.

### Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "gemini_ai": "configured"
}
```

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify Supabase project is active
   - Check Supabase credentials in `.env`
   - Ensure database tables are properly created
   - Check if IP address is allowed in Supabase dashboard

2. **Gemini AI Configuration Error**
   - Verify `GEMINI_API_KEY` is set correctly
   - Check API key permissions and quotas

3. **Story Generation Fails**
   - Check network connectivity
   - Verify Gemini API quotas
   - Review application logs for details

4. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility (3.8+)

### Debug Mode
Set logging level to DEBUG in `config.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Commit your changes: `git commit -am 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review application logs in `app.log`
3. Open an issue on GitHub with detailed error information
4. Include request IDs from error responses for faster debugging

## 🔮 Future Enhancements

- [ ] User authentication and authorization
- [ ] Story templates and themes
- [ ] Character relationship mapping
- [ ] Story continuation and chapters
- [ ] Export stories to different formats (PDF, EPUB)
- [ ] Story rating and feedback system
- [ ] Bulk character import/export
- [ ] Advanced story customization options 