const fs = require('fs');
const path = require('path');
const { GoogleGenerativeAI } = require('@google/generative-ai');

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

function savePosts(posts) {
  try {
    fs.writeFileSync(POSTS_FILE, JSON.stringify(posts, null, 2));
  } catch (e) {
    console.error('Error saving posts:', e);
    throw e;
  }
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const geminiApiKey = process.env.GEMINI_API_KEY;
  if (!geminiApiKey) {
    console.error('GEMINI_API_KEY not set');
    return res.status(500).json({ success: false, error: 'GEMINI_API_KEY not set' });
  }

  try {
    console.log('Initializing Gemini AI...');
    const genAI = new GoogleGenerativeAI(geminiApiKey);
    const model = genAI.getGenerativeModel({ model: 'gemini-2.5-flash' });

    const topics = ["general", "obedience", "submission", "discipline", "control", "worship"];
    const topic = topics[new Date().getHours() % topics.length];

    const prompt = `You are a confident dominatrix on Twitter.
Write a short, teasing, commanding tweet about ${topic}.
Be flirty, dominant, and suggestive but NOT explicit or NSFW.
Use teasing language like "prove yourself", "don't disappoint me", "know your place".
Keep it under 280 characters. No hashtags required.`;

    console.log('Generating content...');
    const result = await model.generateContent(prompt);
    const content = result.response.text().trim();

    const newPost = {
      content,
      time: new Date().toISOString().slice(0, 19).replace('T', ' '),
      generated: true
    };

    console.log('Saving post...');
    const posts = loadPosts();
    posts.push(newPost);
    savePosts(posts);

    res.status(200).json({ success: true, post: newPost });
  } catch (error) {
    console.error('Error generating post:', error);
    res.status(500).json({ success: false, error: error.message, stack: error.stack });
  }
};
