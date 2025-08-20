# LinkedIn Post Automation

A simple app to generate LinkedIn post content and images with AI, preview them, and post to LinkedIn.

## What it uses
- Frontend: React + Tailwind CSS
- Backend: Flask (Python)
- AI:
  - GROQ (LLM) for content generation
  - Hugging Face Inference API for image generation (FLUX.1-dev)
- LinkedIn API: posting to `/v2/ugcPosts`
- Other libs: axios, react-markdown, FontAwesome, flask-cors, requests, Pillow

## Prerequisites
- Node.js and npm
- Python 3.11+
- API keys/tokens:
  - GROQ_API_KEY
  - HUGGINGFACE_API_KEY
  - ACCESS_TOKEN (LinkedIn)
  - PERSON_URN_KEY (e.g., `urn:li:person:xxxx`)

## Setup
1) Backend
- Go to `server/`
- Create and activate venv
- Install deps
- Create `.env` with keys

Example commands:
```
cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# .env (place in server/)
GROQ_API_KEY=your_groq_key
HUGGINGFACE_API_KEY=your_hf_key
ACCESS_TOKEN=your_linkedin_3legged_token
PERSON_URN_KEY=urn:li:person:xxxx
FLASK_ENV=development
PORT=5005
```
Run backend:
```
python wsgi.py
```

2) Frontend
- Go to `client/`
- Install deps
- Create `.env` with backend URL
- Start dev server

Example commands:
```
cd client
npm install

# .env (place in client/)
REACT_APP_BACKEND_URL=http://localhost:5005

npm start
```

## How to use
1. In the app, enter a prompt to generate content.
2. Enter a prompt to generate an image.
3. Preview the post (content + image).
4. Click “Post to LinkedIn”.

## Notes
- Ensure your LinkedIn token has scopes: `openid`, `profile`, `email`, `w_member_social`.
- If image upload fails, text-only post still works.
- If ports are in use, free them or change ports in configs.
