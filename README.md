# Smart Recipe API

A FastAPI-based backend service for managing recipes and generating meal plans.

## Features

- Create and manage recipes with detailed ingredients and instructions
- Search recipes by title or tags
- Generate meal plans based on caloric requirements
- Calculate nutritional information for recipes
- Input validation and error handling
- Async API design for better performance

## Getting Started

1. Clone the repository
2. Install dependencies:   ```bash
   pip install -r requirements.txt   ```
3. Run the server:   ```bash
   uvicorn app.main:app --reload   ```
4. Visit http://localhost:8000/docs for API documentation

## Testing

Run tests using pytest: