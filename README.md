# Xcontent - AI Post Generator

A beautiful dashboard to generate AI-powered social media posts using Google Gemini and manage them locally.

## Features

- Generate AI content with one click
- Beautiful dark UI with smooth animations
- Post history (last 10 posts)
- Copy to clipboard functionality
- Auto-refresh support

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your API key in `config.json`:
   ```json
   {
     "gemini_api_key": "your-api-key-here"
   }
   ```
4. Run the server:
   ```bash
   python server.py
   ```
5. Open http://127.0.0.1:5000

## API Keys Required

- **GEMINI_API_KEY** - For AI content generation (get from Google AI Studio)

## Files

- `server.py` - Flask backend server
- `index.html` - Beautiful dashboard UI
- `twitter_scheduler.py` - AI content generator
- `posts.json` - Local posts storage
