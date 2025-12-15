# Integration Summary

The frontend expects a running backend that exposes the TalentScout API. Point the UI at your backend by setting `VITE_API_BASE_URL` in `.env`.

## Quick Start
1. Start or deploy your backend (default local URL: `http://localhost:8000`).
2. In this repo, create/update `.env`:
   ```bash
   echo "VITE_API_BASE_URL=http://localhost:8000" > .env
   ```
3. Run the frontend:
   ```bash
   npm install
   npm run dev
   ```

## What’s Set Up
- REST-ready UI flow for sessions, chat, and generated questions
- API client utilities under `src/lib/`
- Hooks for conversation state under `src/hooks/`

## Deployment
1. Deploy backend (Railway/Render/Fly.io/any host)
2. Update `VITE_API_BASE_URL` to the deployed backend URL
3. Build and deploy the frontend (Netlify/Vercel/Cloudflare Pages)

