<div align="center">

<img src="./logo.png" alt="LinkedIn Post Automation" width="120" />

# LinkedIn Post Automation

### AI-powered copy, images & one-click posting for LinkedIn

[![Live demo](https://img.shields.io/badge/🌐_Live_Demo-GitHub_Pages-0A66C2?style=for-the-badge)](https://zishan23.github.io/LinkedIn-Post-Automation-Powered-by-AI/)
[![Repo](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/Zishan23/LinkedIn-Post-Automation-Powered-by-AI)

<br/>

![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-API-000000?style=flat-square&logo=flask&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind-CSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)
![GROQ](https://img.shields.io/badge/GROQ-LLM-F55036?style=flat-square)
![HuggingFace](https://img.shields.io/badge/Hugging_Face-FLUX-FFD21E?style=flat-square&logo=huggingface&logoColor=black)
![LinkedIn](https://img.shields.io/badge/LinkedIn-UGC_API-0A66C2?style=flat-square&logo=linkedin&logoColor=white)

<br/>

**[Open the live app →](https://zishan23.github.io/LinkedIn-Post-Automation-Powered-by-AI/)** · Works as a **static UI demo** (mock AI & posting). Run the stack locally for real GROQ, FLUX, and LinkedIn.

</div>

---

## Preview

<table>
  <tr>
    <td align="center" width="50%">
      <img src="docs/screenshots/01.png" alt="App screenshot 1" width="100%" />
    </td>
    <td align="center" width="50%">
      <img src="docs/screenshots/02.png" alt="App screenshot 2" width="100%" />
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="docs/screenshots/03.png" alt="App screenshot 3" width="100%" />
    </td>
    <td align="center">
      <img src="docs/screenshots/04.png" alt="App screenshot 4" width="100%" />
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="docs/screenshots/05.png" alt="App screenshot 5" width="100%" />
    </td>
    <td align="center">
      <img src="docs/screenshots/06.png" alt="App screenshot 6" width="100%" />
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="docs/screenshots/07.jpg" alt="App screenshot 7" width="100%" />
    </td>
    <td align="center">
      <img src="docs/screenshots/08.png" alt="App screenshot 8" width="100%" />
    </td>
  </tr>
</table>

---

## What it does

1. **Content** — User enters a topic; the backend runs a short **multi-agent** chat (generator + critic) backed by **GROQ** (Llama 3) to produce polished LinkedIn-style text.
2. **Image** — User enters an image prompt; **Hugging Face Inference API** (FLUX.1-dev) generates an image; the API returns PNG bytes.
3. **Preview** — React UI shows markdown-rendered copy and the image together, with a lightweight schedule control in the timeline.
4. **Post** — Backend registers an upload with LinkedIn, uploads the asset when present, and creates a **UGC post** (`/v2/ugcPosts`). Text-only fallback if image upload fails.

## Tech stack

| Layer | Technologies |
|--------|----------------|
| **Frontend** | React 18, Create React App, Tailwind CSS, Axios, react-markdown, Font Awesome, react-hot-toast, lucide-react |
| **Backend** | Python 3.11+, Flask, flask-cors, asyncio |
| **AI — LLM** | Microsoft AutoGen AgentChat (`RoundRobinGroupChat`), GROQ OpenAI-compatible API (`llama3-70b-8192`) |
| **AI — image** | Hugging Face Inference API — `black-forest-labs/FLUX.1-dev` |
| **Integrations** | LinkedIn REST (`/v2/ugcPosts`, asset register/upload) |
| **Research / extras** | `analysis/` — interpretability-style scripts (e.g. LIME/SHAP); optional for running the app |

## Architecture

```mermaid
flowchart LR
  subgraph client [React client]
    UI[Landing / Timeline / Preview]
  end
  subgraph api [Flask API]
    GC["/api/v1/generate-content"]
    GI["/api/v1/generate-image"]
    PL["/api/v1/post-linkedin"]
  end
  subgraph agents [AutoGen team]
    A1[Content agent]
    A2[Critic agent]
  end
  UI --> GC
  UI --> GI
  UI --> PL
  GC --> agents
  agents --> GROQ[GROQ LLM]
  GI --> HF[Hugging Face FLUX]
  PL --> LI[LinkedIn API]
```

- **`client/src/components/Timeline.js`** — Orchestrates schedule state, `ContentQuery`, `ImageQuery`, and `Preview`.
- **`server/wsgi.py`** — REST routes; image route returns `generated_image.png` from disk after generation.
- **`server/services/generate_content.py`** — `RoundRobinGroupChat` with `MaxMessageTermination(max_messages=3)` between `content_generation_agent` and `critic_agent`.
- **`server/services/post_linkedin.py`** — Register upload → PUT image → build `ugcPosts` payload (image or text-only).

## Live demo & deploy

| Environment | URL | Notes |
|-------------|-----|--------|
| **GitHub Pages** | [zishan23.github.io/LinkedIn-Post-Automation-Powered-by-AI](https://zishan23.github.io/LinkedIn-Post-Automation-Powered-by-AI/) | Static UI; mock generation when API is unavailable. |
| **Full stack** | Run locally (below) | Real GROQ, Hugging Face FLUX, and LinkedIn posting. |

CI deploys the `client` build to GitHub Pages on push to **`master`** or **`main`**. Manual deploy: see [DEPLOYMENT.md](./DEPLOYMENT.md).

## Prerequisites

- Node.js and npm (Node 18+ for CI / Pages build)
- Python 3.11+
- API keys / tokens:
  - `GROQ_API_KEY`
  - `HUGGINGFACE_API_KEY`
  - `ACCESS_TOKEN` (LinkedIn OAuth, 3-legged, with posting scopes)
  - `PERSON_URN_KEY` (e.g. `urn:li:person:xxxx`)

## Setup

### 1) Backend

```bash
cd server
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `server/.env`:

```env
GROQ_API_KEY=your_groq_key
HUGGINGFACE_API_KEY=your_hf_key
ACCESS_TOKEN=your_linkedin_token
PERSON_URN_KEY=urn:li:person:xxxx
FLASK_ENV=development
PORT=5005
```

Run:

```bash
python wsgi.py
```

### 2) Frontend

```bash
cd client
npm install
```

Create `client/.env`:

```env
REACT_APP_BACKEND_URL=http://localhost:5005
```

Start:

```bash
npm start
```

### GitHub Pages / demo build

The client sets `homepage` for gh-pages. For a **static demo**, `client/src/config/demo.js` provides mock flows when the backend is unreachable. See [DEPLOYMENT.md](./DEPLOYMENT.md).

## How to use

1. Enter a prompt to generate post content.
2. Enter a prompt to generate an image (optional).
3. Review the preview.
4. Click **Post to LinkedIn** (full stack only, with valid token and URN).

## Notes

- LinkedIn token scopes should include: `openid`, `profile`, `email`, `w_member_social`.
- If image upload fails, a text-only post is still attempted.
- Change ports if `5005` or the React dev port is in use.

## Security

- Keep all secrets in `.env` files; do not commit them.
- If this repo was ever public with credentials in code, **rotate** those keys in the provider dashboards.

## License / attribution

Add a license file if you want open-source terms; otherwise default GitHub copyright applies.
