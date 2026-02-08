const { put } = require('@vercel/blob');
const { GoogleGenerativeAI } = require('@google/generative-ai');

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const geminiApiKey = process.env.GEMINI_API_KEY;
  if (!geminiApiKey) {
    return res.status(500).json({ success: false, error: 'GEMINI_API_KEY not set in Vercel' });
  }

  try {
    const genAI = new GoogleGenerativeAI(geminiApiKey);
    const model = genAI.getGenerativeModel({ model: 'gemini-2.5-flash' });

    const topics = ["general", "obedience", "submission", "discipline", "control", "worship"];
    const topic = topics[new Date().getHours() % topics.length];

    const prompt = `You are a confident dominatrix on Twitter.
Write a short, teasing, commanding tweet about ${topic}.
Be flirty, dominant, and suggestive but NOT explicit or NSFW.
Use teasing language like "prove yourself", "don't disappoint me", "know your place".
Keep it under 280 characters. No hashtags required.`;

    const result = await model.generateContent(prompt);
    const content = result.response.text().trim();

    const newPost = {
      content,
      time: new Date().toISOString().slice(0, 19).replace('T', ' '),
      generated: true
    };

    let posts = [];
    try {
      const existing = await fetch('https://public.blob.vercel-storage.com/posts.json');
      posts = await existing.json();
    } catch (e) {}

    posts.push(newPost);
    await put('posts.json', JSON.stringify(posts, null, 2), { access: 'public' });

    res.status(200).json({ success: true, post: newPost });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
};
