# Frontend-Backend Integration Guide

This guide explains how to connect the React frontend with a Python FastAPI (or similar) backend that exposes the TalentScout endpoints.

## Project Structure

```
hiringbot/              # Frontend (React/TypeScript)
├── src/
│   ├── lib/            # API client utilities
│   └── hooks/          # Conversation state hooks
└── ...
```

## Setup Steps

### 1) Backend Setup (reference)
- Ensure your backend exposes the endpoints used by the app (sessions, message, generate-questions).
- Run locally, e.g.: `uvicorn api:app --reload --port 8000`
- Confirm it is reachable at `http://localhost:8000` (or your chosen port).

### 2) Frontend Setup
1. Create `.env`:
   ```bash
   echo "VITE_API_BASE_URL=http://localhost:8000" > .env
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the dev server:
   ```bash
   npm run dev
   ```

### 3) Testing the Connection
1. Open the app at `http://localhost:5173` (default Vite port).
2. Start a session; chat requests should hit the backend.
3. Validate generated questions and chat flow.

## Repositories
You can keep frontend and backend together or separate. The frontend only needs the backend URL via `VITE_API_BASE_URL`.

## Deployment
- **Backend:** Deploy to your host of choice and note the public URL.
- **Frontend:** `npm run build`, then deploy `dist/` to Netlify/Vercel/Cloudflare Pages.
- Set `VITE_API_BASE_URL` in the hosting environment to your backend URL.

## API Endpoints (expected)
- `POST /api/sessions` — Create new session
- `GET /api/sessions/{session_id}` — Fetch session info
- `POST /api/message` — Send message to chatbot
- `POST /api/generate-questions` — Generate questions

See `API_DOCS.md` for details.

## Troubleshooting
- CORS errors: confirm backend CORS config and `VITE_API_BASE_URL`.
- Connection refused: ensure backend is running and URL/port match.
- Session not found: clear localStorage and try again.

## Development Workflow
1. Start backend
2. Start frontend with `npm run dev`
3. Make changes; both hot-reload
4. Test locally before deploying

