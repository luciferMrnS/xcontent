const { put, del, list } = require('@vercel/blob');

module.exports = async (req, res) => {
  try {
    const { blobs } = await list();
    
    let posts = [];
    const postsBlob = blobs.find(b => b.pathname === 'posts.json');
    
    if (postsBlob) {
      const response = await fetch(postsBlob.url);
      posts = await response.json();
    }
    
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
