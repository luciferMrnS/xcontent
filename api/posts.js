const fs = require('fs');
const path = require('path');

const POSTS_FILE = '/tmp/posts.json';

function loadPosts() {
  try {
    if (fs.existsSync(POSTS_FILE)) {
      return JSON.parse(fs.readFileSync(POSTS_FILE, 'utf8'));
    }
  } catch (e) {
    console.error('Error loading posts:', e);
    return [];
  }
  return [];
}

module.exports = (req, res) => {
  try {
    const posts = loadPosts();
    const sortedPosts = posts.sort((a, b) => new Date(b.time) - new Date(a.time));
    
    res.status(200).json({
      all_posts: sortedPosts,
      history: sortedPosts.slice(0, 10),
      stats: {
        total: sortedPosts.length,
        generated: sortedPosts.filter(p => p.generated).length
      }
    });
  } catch (error) {
    console.error('Error in posts API:', error);
    res.status(500).json({ error: error.message });
  }
};
