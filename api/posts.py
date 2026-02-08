import os
import json
from datetime import datetime

POSTS_FILE = 'posts.json'

def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'r') as f:
            return json.load(f)
    return []

def handler(request):
    posts = load_posts()
    sorted_posts = sorted(posts, key=lambda x: datetime.fromisoformat(x['time']), reverse=True)
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'all_posts': sorted_posts,
            'history': sorted_posts[:10],
            'stats': {
                'total': len(sorted_posts),
                'generated': len([p for p in sorted_posts if p.get('generated')])
            }
        })
    }
