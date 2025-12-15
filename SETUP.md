# Setup Guide - TalentScout AI

## Quick Setup (5 minutes)

### 1. Install Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

**Root (for running both):**
```bash
npm install
```

### 2. Configure Environment

**Backend:**
```bash
cd backend
cp env.example .env
# Edit .env and add your OPENAI_API_KEY
```

**Frontend:**
The `.env` file is already created with:
```
VITE_API_BASE_URL=http://localhost:8000
```

### 3. Start the Application

**Option A: Use the startup script (easiest):**
```bash
./start.sh
```

**Option B: Use npm script:**
```bash
npm run dev
```

**Option C: Run separately:**

Terminal 1:
```bash
cd backend
python api.py
```

Terminal 2:
```bash
cd frontend
npm run dev
```

### 4. Access the Application

- **Frontend UI:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## Verification

1. ✅ Backend should show: "Application startup complete"
2. ✅ Frontend should open in browser
3. ✅ You should see the chat interface
4. ✅ Try sending a message - it should connect to backend

## Troubleshooting

### Backend Issues

**Import errors:**
- Make sure you're in the `backend/` directory when running
- Check that all dependencies are installed: `pip install -r requirements.txt`

**Port 8000 already in use:**
- Change port in `backend/api.py`: `uvicorn.run(app, host="0.0.0.0", port=8001)`
- Update frontend `.env`: `VITE_API_BASE_URL=http://localhost:8001`

**Missing OPENAI_API_KEY:**
- Create `backend/.env` file
- Add: `OPENAI_API_KEY=your_key_here`

### Frontend Issues

**Can't connect to backend:**
- Check backend is running on port 8000
- Verify `frontend/.env` has correct URL
- Check browser console for errors

**Port 5173 already in use:**
- Vite will automatically use next available port
- Check terminal output for actual port

**Module not found:**
- Run `npm install` in `frontend/` directory
- Delete `node_modules` and reinstall if needed

## Next Steps

1. ✅ Test the chat interface
2. ✅ Verify field collection works
3. ✅ Check question generation
4. ✅ Test on different devices/browsers

## Production Deployment

See main README.md for deployment instructions.

