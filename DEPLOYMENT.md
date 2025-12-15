# Deployment Guide - TalentScout AI

## ✅ Pre-Deployment Checklist

Your project is now **ready for Netlify deployment**! The following issues have been resolved:

- ✅ Removed duplicate frontend files from root directory
- ✅ Fixed Netlify configuration (`netlify.toml`)
- ✅ Fixed CSS import order warning
- ✅ Build process verified and working
- ✅ Git repository cleaned and committed

## 🚀 Deploying to Netlify

### Option 1: Netlify UI (Recommended for First Deployment)

1. **Push your code to GitHub** (if not already done):
   ```bash
   git push origin main
   ```

2. **Go to [Netlify](https://app.netlify.com/)**
   - Sign in or create an account
   - Click "Add new site" → "Import an existing project"

3. **Connect to GitHub**
   - Select your repository: `riteshdhobale/talentbot-ai`
   - Branch: `main`

4. **Build Settings** (should auto-detect from `netlify.toml`):
   - Base directory: `frontend`
   - Build command: `npm install && npm run build`
   - Publish directory: `frontend/dist`

5. **Environment Variables** (Optional - for backend integration):
   - Add: `VITE_API_BASE_URL` = `https://your-backend-url.com`
   - If no backend yet, you can skip this

6. **Deploy!**
   - Click "Deploy site"
   - Wait 2-3 minutes for the build to complete

### Option 2: Netlify CLI

```bash
# Install Netlify CLI (if not installed)
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy from project root
netlify deploy

# When prompted:
# - Create & configure new site
# - Deploy path: frontend/dist

# For production deployment
netlify deploy --prod
```

## 📋 Current Configuration

### netlify.toml
```toml
[build]
  base = "frontend"
  command = "npm install && npm run build"
  publish = "frontend/dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Project Structure
```
hiringbot/
├── backend/              # Python FastAPI backend
├── frontend/             # React + TypeScript frontend
│   ├── src/
│   ├── public/
│   ├── dist/            # Build output (gitignored)
│   └── package.json
├── netlify.toml          # Netlify configuration
└── package.json          # Root package.json
```

## 🔧 Environment Variables

If you need to connect to a backend API, set this in Netlify:

**Variable Name:** `VITE_API_BASE_URL`  
**Value:** Your backend URL (e.g., `https://api.yoursite.com`)

**How to set in Netlify:**
1. Go to: Site settings → Environment variables
2. Add variable → `VITE_API_BASE_URL`
3. Save and redeploy

## 🧪 Testing Locally Before Deployment

```bash
# From project root
cd frontend

# Install dependencies
npm install

# Build for production
npm run build

# Preview production build
npm run preview
```

Visit the preview URL to test your build locally.

## 🐛 Troubleshooting

### Build fails on Netlify

1. **Check build logs** in Netlify dashboard
2. **Common issues:**
   - Missing dependencies → Check `frontend/package.json`
   - Environment variables → Verify in Netlify settings
   - Node version → Netlify uses Node 18+ by default

### To specify Node version (if needed)

Create `.nvmrc` in the `frontend/` folder:
```
18.18.0
```

### Build works locally but fails on Netlify

- Clear Netlify cache: Deploy settings → "Clear cache and retry deploy"
- Check for case-sensitive file imports (Linux/Mac vs Windows)

## 📦 Backend Deployment

The frontend is a static site, but your backend (`backend/`) needs separate hosting:

**Options:**
- **Railway** (recommended for Python/FastAPI)
- **Render**
- **Heroku**
- **AWS/GCP/Azure**

After deploying backend, update `VITE_API_BASE_URL` in Netlify.

## 🎉 Post-Deployment

After successful deployment:

1. ✅ Test all features on the live site
2. ✅ Check browser console for errors
3. ✅ Verify API calls work (if backend connected)
4. ✅ Test on mobile devices
5. ✅ Set up custom domain (optional)

## 🔄 Continuous Deployment

Netlify automatically deploys when you push to `main`:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Netlify will detect the push and redeploy automatically.

## 📝 Notes

- Build time: ~2-3 minutes
- The site is a SPA (Single Page Application)
- All routes redirect to `index.html` (configured in `netlify.toml`)
- Frontend runs independently of backend
