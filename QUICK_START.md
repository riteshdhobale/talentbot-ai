# 🚀 Quick Start Guide

## ✅ Setup Complete!

Everything is configured and ready to run.

## ⚠️ Important: Add Your OpenAI API Key

Before running, you need to add your OpenAI API key:

```bash
# Edit the backend .env file
cd backend
nano .env
# Or use any text editor

# Change this line:
OPENAI_API_KEY=your_openai_api_key_here

# To:
OPENAI_API_KEY=sk-your-actual-key-here
```

## 🎯 Start the Application

### Option 1: Run Both Together (Recommended)
```bash
npm run dev
```

### Option 2: Use the Startup Script
```bash
./start.sh
```

### Option 3: Run Separately

**Terminal 1 - Backend:**
```bash
cd backend
python3 api.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## 🌐 Access Points

Once running:
- **Frontend UI:** http://localhost:5173 (or check terminal for actual port)
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## ✅ Verification Checklist

- [x] Backend structure organized
- [x] Frontend dependencies installed
- [x] Environment files created
- [x] Backend imports working
- [ ] **Add OpenAI API key to `backend/.env`** ← YOU NEED TO DO THIS
- [ ] Start the application
- [ ] Test the chat interface

## 🧪 Test It

1. Open http://localhost:5173 in your browser
2. You should see the chat interface
3. Start typing - the bot should respond
4. Check the browser console (F12) for any errors
5. Check backend terminal for API logs

## 🐛 Troubleshooting

**Backend won't start:**
- Make sure you added your OpenAI API key
- Check: `cd backend && python3 api.py`

**Frontend can't connect:**
- Make sure backend is running on port 8000
- Check `frontend/.env` has: `VITE_API_BASE_URL=http://localhost:8000`

**Port conflicts:**
- Backend: Change port in `backend/api.py`
- Frontend: Vite will auto-use next available port

## 📚 More Help

- See `README.md` for full documentation
- See `SETUP.md` for detailed setup
- See `backend/API_DOCS.md` for API details

