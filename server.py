from flask import Flask, jsonify, send_from_directory
import subprocess
import json
import os
from datetime import datetime

app = Flask(__name__, static_folder='.')

POSTS_FILE = 'posts.json'

def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_posts(posts):
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f, indent=2)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/posts')
def get_posts():
    posts = load_posts()
    sorted_posts = sorted(posts, key=lambda x: datetime.fromisoformat(x['time']), reverse=True)
    return jsonify({
        'all_posts': sorted_posts,
        'history': sorted_posts[:10],
        'stats': {
            'total': len(sorted_posts),
            'generated': len([p for p in sorted_posts if p.get('generated')])
        }
    })

@app.route('/api/generate', methods=['POST'])
def generate_post():
    result = subprocess.run(['python', 'twitter_scheduler.py'], capture_output=True, text=True)
    
    if result.returncode == 0:
        posts = load_posts()
        sorted_posts = sorted(posts, key=lambda x: datetime.fromisoformat(x['time']), reverse=True)
        new_post = sorted_posts[0] if sorted_posts else None
        return jsonify({'success': True, 'post': new_post})
    else:
        return jsonify({'success': False, 'error': result.stderr}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
