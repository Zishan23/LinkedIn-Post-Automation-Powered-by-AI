// Demo configuration for GitHub Pages deployment
// This file provides mock functionality when the backend is not available

export const DEMO_MODE = true;

// Mock content generation
export const generateMockContent = (prompt) => {
  const mockPosts = {
    'ai': `🚀 **The AI Revolution is Here!**

Artificial Intelligence is transforming every industry, from healthcare to finance. Here's what excites me most:

• **Automation**: Streamlining repetitive tasks
• **Insights**: Uncovering hidden patterns in data  
• **Innovation**: Creating solutions we never imagined

What's your take on AI? Are you excited or concerned about its impact on your field?

Share your thoughts below! 👇

#AI #Innovation #FutureOfWork #Technology`,
    
    'marketing': `💡 **Digital Marketing Secrets That Actually Work**

After years in the industry, here are the 3 strategies that consistently deliver results:

🎯 **Content is King**: Quality over quantity every time
📱 **Mobile-First**: Your audience is on mobile devices
📊 **Data-Driven**: Let analytics guide your decisions

The key? Consistency and authenticity.

What marketing tactic has worked best for you? Drop your insights in the comments!

#DigitalMarketing #MarketingTips #Growth #Strategy`,
    
    'technology': `⚡ **Tech Trends That Will Shape 2025**

The future is arriving faster than ever! Here's what's on my radar:

🔮 **AI Integration**: Seamless AI in everyday tools
🌐 **Web3 Evolution**: Beyond the hype, real applications
🔒 **Cybersecurity**: Protecting our digital lives

Technology should solve real problems, not create new ones.

Which tech trend are you most excited about? Let's discuss!

#Technology #Innovation #TechTrends #Future`,
    
    'default': `✨ **Creating Meaningful Content**

Every post is an opportunity to connect, inspire, and add value to someone's day.

The best content comes from:
• Authentic experiences
• Genuine insights
• Real conversations

What story do you want to share today?

#ContentCreation #Authenticity #Connection #Growth`
  };

  // Find the best match for the prompt
  const promptLower = prompt.toLowerCase();
  let bestMatch = 'default';
  
  for (const topicKey of Object.keys(mockPosts)) {
    if (promptLower.includes(topicKey)) {
      bestMatch = topicKey;
      break;
    }
  }

  return {
    success: true,
    content: mockPosts[bestMatch],
    message: "Demo content generated successfully!"
  };
};

// Mock image generation
export const generateMockImage = (prompt) => {
  const mockImages = {
    'ai': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=600&fit=crop',
    'marketing': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=600&fit=crop',
    'technology': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=600&fit=crop',
    'default': 'https://images.unsplash.com/photo-1551434678-e076c223a692?w=800&h=600&fit=crop'
  };

  const promptLower = prompt.toLowerCase();
  let bestMatch = 'default';
  
  for (const topicKey of Object.keys(mockImages)) {
    if (promptLower.includes(topicKey)) {
      bestMatch = topicKey;
      break;
    }
  }

  return {
    success: true,
    imageUrl: mockImages[bestMatch],
    message: "Demo image generated successfully!"
  };
};

// Mock LinkedIn posting
export const mockLinkedInPost = (content, imageUrl) => {
  return {
    success: true,
    message: "Demo: Post would be published to LinkedIn!",
    postId: "demo-post-" + Date.now(),
    content: content,
    imageUrl: imageUrl
  };
};

// Demo mode indicator
export const showDemoMode = () => {
  return {
    title: "Demo Mode",
    description: "This is a demonstration version running on GitHub Pages. The full application with AI-powered content generation and LinkedIn posting requires the backend server.",
    features: [
      "Mock content generation based on your prompts",
      "Sample images from Unsplash",
      "Simulated LinkedIn posting",
      "Full UI/UX demonstration"
    ]
  };
}; 