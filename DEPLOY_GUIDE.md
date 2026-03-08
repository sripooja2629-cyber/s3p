# 🚀 NCERT Study Buddy — Deploy to Internet (Render.com)

## Your Domain: sp3j0zo.com
## Free Hosting: Render.com

---

## STEP 1: Create GitHub Account & Upload Project

1. Go to **https://github.com** → Sign up (free)
2. Click **"New Repository"**
3. Name it: `ncert-chatbot`
4. Click **"Create Repository"**
5. Upload your project folder

---

## STEP 2: Deploy Backend on Render

1. Go to **https://render.com** → Sign up with GitHub
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo `ncert-chatbot`
4. Settings:
   - **Name:** `ncert-chatbot-backend`
   - **Runtime:** Docker
   - **Start Command:** `uvicorn backend.api.main:app --host 0.0.0.0 --port $PORT`
5. Click **"Create Web Service"**
6. Wait 5-10 mins for build
7. You get URL like: `https://ncert-chatbot-backend.onrender.com`

---

## STEP 3: Deploy Frontend on Render

1. Click **"New +"** → **"Web Service"** again
2. Same GitHub repo
3. Settings:
   - **Name:** `ncert-chatbot-frontend`
   - **Start Command:** `streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0`
   - **Environment Variable:** `FASTAPI_URL` = `https://ncert-chatbot-backend.onrender.com`
4. Click **"Create Web Service"**
5. You get URL like: `https://ncert-chatbot-frontend.onrender.com`

---

## STEP 4: Connect Your Domain sp3j0zo.com

1. In Render → your frontend service → **"Custom Domains"**
2. Add: `sp3j0zo.com`
3. Render gives you a CNAME record
4. Go to your domain registrar → DNS Settings
5. Add the CNAME record Render gives you
6. Wait 1-24 hours for DNS propagation

---

## Result:
- 🌐 **http://sp3j0zo.com** → Your NCERT Study Buddy live!
