import os
import json
import google.generativeai as genai
from datetime import datetime

POSTS_FILE = 'posts.json'

def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_posts(posts):
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f, indent=2)

def generate_content():
    gemini_api_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('VERCEL_GEMINI_API_KEY')
    if not gemini_api_key:
        return {'success': False, 'error': 'GEMINI_API_KEY not set'}
    
    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        topics = ["general", "obedience", "submission", "discipline", "control", "worship"]
        topic = topics[datetime.now().hour % len(topics)]
        
        prompt = f"""You are a confident dominatrix on Twitter.
Write a short, teasing, commanding tweet about {topic}.
Be flirty, dominant, and suggestive but NOT explicit or NSFW.
Use teasing language like "prove yourself", "don't disappoint me", "know your place".
Keep it under 280 characters. No hashtags required."""
        
        response = model.generate_content(prompt)
        content = response.text.strip()
        
        new_post = {
            'content': content,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'generated': True
        }
        
        posts = load_posts()
        posts.append(new_post)
        save_posts(posts)
        
        return {'success': True, 'post': new_post}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def handler(request):
    result = generate_content()
    return {
        'statusCode': 200 if result['success'] else 500,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(result)
    }
