const { kv } = require('@vercel/kv');

async function loadPosts() {
  try {
    const posts = await kv.get('posts');
    return posts || [];
  } catch (e) {
    console.error('Error loading posts:', e);
    return [];
  }
}

module.exports = async (req, res) => {
  try {
    const posts = await loadPosts();
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
