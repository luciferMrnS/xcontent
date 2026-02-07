import os
import time
import json
import logging
from datetime import datetime
import requests
import google.generativeai as genai
from requests_oauthlib import OAuth1
from typing import List, Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TwitterScheduler:
    def __init__(self, config_file: str = 'config.json'):
        self.config_file = config_file
        self.config = self.load_config()
        self.bearer_token = os.environ.get('TWITTER_BEARER_TOKEN') or self.config.get('bearer_token')
        self.api_key = os.environ.get('TWITTER_API_KEY') or self.config.get('api_key')
        self.api_secret = os.environ.get('TWITTER_API_SECRET') or self.config.get('api_secret')
        self.access_token = os.environ.get('TWITTER_ACCESS_TOKEN') or self.config.get('access_token')
        self.access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET') or self.config.get('access_token_secret')
        self.base_url = 'https://api.twitter.com/2'
        self.gemini_api_key = os.environ.get('GEMINI_API_KEY') or self.config.get('gemini_api_key')
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)

    def load_config(self) -> dict:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load config file: {e}")
        return {}

    def get_oauth1_headers(self) -> dict:
        import base64
        from urllib.parse import quote
        import hmac
        import hashlib

        oauth_consumer_key = self.api_key
        oauth_token = self.access_token
        oauth_signature_method = 'HMAC-SHA1'
        oauth_timestamp = str(int(time.time()))
        oauth_nonce = base64.b64encode(os.urandom(16)).decode('utf-8')
        oauth_nonce = oauth_nonce.replace('=', 'A').replace('+', '0').replace('/', '0')

        oauth_params = {
            'oauth_consumer_key': oauth_consumer_key,
            'oauth_token': oauth_token,
            'oauth_signature_method': oauth_signature_method,
            'oauth_timestamp': oauth_timestamp,
            'oauth_nonce': oauth_nonce,
            'oauth_version': '1.0'
        }
        return oauth_params

    def post_tweet(self, text: str) -> Optional[dict]:
        url = f'{self.base_url}/tweets'
        payload = {'text': text}
        auth = OAuth1(
            self.api_key,
            client_secret=self.api_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
            signature_method='HMAC-SHA1'
        )

        try:
            response = requests.post(url, json=payload, auth=auth)
            if response.status_code in [200, 201]:
                logger.info(f"Tweet posted successfully: {text[:50]}...")
                return response.json()
            else:
                logger.error(f"Failed to post tweet: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            return None

    def generate_and_save_content(self, topic: str = "general", posts_file: str = 'posts.json'):
        content = self.generate_dominatrix_content(topic)
        if content:
            new_post = {
                'content': content,
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'generated': True
            }
            
            existing_posts = []
            if os.path.exists(posts_file):
                try:
                    with open(posts_file, 'r') as f:
                        existing_posts = json.load(f)
                except:
                    pass
            
            existing_posts.append(new_post)
            
            with open(posts_file, 'w') as f:
                json.dump(existing_posts, f, indent=2)
            
            logger.info(f"Generated and saved: {content[:50]}...")
            return content
        return None

    def create_sample_posts(self, filename: str):
        sample_posts = [
            {
                'content': 'Hello World! This is my first automated tweet! #automation #python',
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'content': 'Scheduled posting is easy with Python! #coding',
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        ]
        with open(filename, 'w') as f:
            json.dump(sample_posts, f, indent=2)
        logger.info(f"Sample posts file created: {filename}")

    def generate_dominatrix_content(self, topic: str = "general") -> Optional[str]:
        if not self.gemini_api_key:
            logger.warning("GEMINI_API_KEY not set")
            return None

        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            prompt = f"""You are a confident dominatrix on Twitter.
Write a short, teasing, commanding tweet about {topic}.
Be flirty, dominant, and suggestive but NOT explicit or NSFW.
Use teasing language like "prove yourself", "don't disappoint me", "know your place".
Keep it under 280 characters. No hashtags required."""
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            return None

def main():
    scheduler = TwitterScheduler()

    if not scheduler.gemini_api_key:
        logger.error("GEMINI_API_KEY not set. Cannot generate content.")
        return

    topics = ["general", "obedience", "submission", "discipline", "control", "worship"]
    topic = topics[datetime.now().hour % len(topics)]
    content = scheduler.generate_and_save_content(topic)
    if content:
        logger.info(f"Content saved to posts.json - ready for manual posting")
    else:
        logger.error("Failed to generate content")

if __name__ == '__main__':
    main()
