# TalentScout – AI Hiring Assistant

Modern full-stack web application for collecting candidate information and generating tailored technical questions through an AI-assisted chat experience.

## 🌟 Features
- Conversational UI with typing indicators and progress steps
- Guided question list plus freeform chat
- Privacy banner and consent notice
- Generated technical questions tailored to the candidate
- Responsive layout with shadcn/ui + Tailwind
- FastAPI backend with LLM integration

## 🛠️ Tech Stack

### Frontend
- React + TypeScript (Vite)
- shadcn/ui components + Tailwind CSS
- React Query for API state management
- Custom hooks and form validation

### Backend
- Python FastAPI
- LLM integration for intelligent question generation
- Session management
- RESTful API

## 📁 Project Structure
```
hiringbot/
├── frontend/           # React TypeScript frontend
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── pages/
│   │   └── types/
│   ├── public/
│   └── package.json
├── backend/            # Python FastAPI backend
│   ├── api.py
│   ├── core/
│   ├── tests/
│   └── requirements.txt
├── netlify.toml        # Netlify deployment config
├── DEPLOYMENT.md       # Deployment instructions
└── package.json        # Root scripts
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.9+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/riteshdhobale/talentbot-ai.git
   cd talentbot-ai
   ```

2. **Install Frontend Dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Install Backend Dependencies**
   ```bash
   cd ../backend
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   
   Frontend (optional):
   ```bash
   cd frontend
   cp .env.example .env
   # Edit .env if needed
   ```

   Backend:
   ```bash
   cd backend
   cp env.example .env
   # Edit .env with your API keys
   ```

### 🏃 Running the Application

#### Option 1: Run Both (Frontend + Backend)
```bash
# From project root
npm run dev
```

#### Option 2: Run Separately

**Backend:**
```bash
cd backend
python api.py
```
Runs on http://localhost:8000

**Frontend:**
```bash
cd frontend
npm run dev
```
Runs on http://localhost:5173

### 🏗️ Building for Production

```bash
# Build frontend
cd frontend
npm run build
```
Output: `frontend/dist/`

## 📦 Deployment

See **[DEPLOYMENT.md](./DEPLOYMENT.md)** for complete deployment instructions.

### Quick Deploy to Netlify

1. Push to GitHub
2. Connect repository to Netlify
3. Configuration is already set in `netlify.toml`
4. Deploy!

**Build Settings:**
- Base directory: `frontend`
- Build command: `npm install && npm run build`
- Publish directory: `frontend/dist`

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests (add your test setup)
cd frontend
npm test
```

## 📜 Available Scripts

### Root
- `npm run dev` — Run both frontend and backend
- `npm run build` — Build frontend for production
- `npm run install:all` — Install all dependencies

### Frontend
- `npm run dev` — Start Vite dev server
- `npm run build` — Production build
- `npm run preview` — Preview production build
- `npm run lint` — Lint code

### Backend
- `python api.py` — Start FastAPI server

## 🔑 Environment Variables

### Frontend
- `VITE_API_BASE_URL` — Backend API URL (default: http://localhost:8000)

### Backend
- See `backend/env.example` for required variables

## 📚 Documentation

- [API Documentation](./API_DOCS.md)
- [Deployment Guide](./DEPLOYMENT.md)
- [Quick Start](./QUICK_START.md)
- [Project Summary](./PROJECT_SUMMARY.md)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License
MIT

## 👨‍💻 Author
Ritesh Dhobale - [@riteshdhobale](https://github.com/riteshdhobale)

---

**Status:** ✅ Ready for deployment

