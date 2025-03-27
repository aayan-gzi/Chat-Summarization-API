Chat Summarization API 🚀

This is a FastAPI-based backend that stores user chats, retrieves them, and generates summaries using an LLM-powered model.

## Features
- ✅ Store & retrieve chat messages
- ✅ Chat summarization using an LLM (Spent 5 hours debugging, but still not working)
- ✅ Pagination for efficient chat retrieval (Not showing on FastAPI Swagger UI)
- ✅ Optimized CRUD operations with PostgreSQL

## Tech Stack 🛠️
- FastAPI ⚡
- PostgreSQL 🗄️
- OpenAI API (for summarization) 🤖

## Installation 🏗️
1. Clone the repository:  
   ```sh
   git clone https://github.com/aayan-gzi/chat-summarization-api.git
   cd chat-summarization-api
2. Install Dependencies
   ```sh
   pip install -r requirements.txt
3. Set Up Environment Variables
   ```sh
   Create a `.env` file in the project root and add:
   DATABASE_URL=postgresql://user:password@localhost:5432/db_name
   OPENROUTER_API_KEY=your_api_key_here

4. Run Database Migrations
   ```sh
   alembic upgrade head
5. Start the FastAPI Server
   ```sh
   uvicorn main:app --reload

The API will run at http://127.0.0.1:8000
Base URL: http://127.0.0.1:8000
Swagger UI: http://127.0.0.1:8000/docs
