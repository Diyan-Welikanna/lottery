# Free Hosting Options for Sri Lankan Lottery Scraper

## Quick Recommendation
**Best Free Option**: **Render.com** (Free tier includes database!)

---

## Option 1: Render.com ⭐ RECOMMENDED

### Why Render?
- ✅ **Free Tier**: 750 hours/month (enough for 24/7)
- ✅ **Includes PostgreSQL Database** (Free tier: 90 days, then auto-renew)
- ✅ **Auto-deploys from GitHub**
- ✅ **Persistent storage** for SQLite (with caveats)
- ✅ **HTTPS included**
- ✅ **Background workers supported**
- ⚠️ Sleeps after 15 minutes of inactivity (Free tier)
- ⚠️ Cold start takes 30-60 seconds

### Deployment Steps

#### 1. **Prepare Your Code**

Create `render.yaml` in your project root:
```yaml
services:
  - type: web
    name: lottery-scraper-api
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: python main.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.11
      - key: PORT
        value: 8000
```

#### 2. **Update `main.py`** to bind to Render's PORT:
```python
import os

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

#### 3. **Update Database Path** for persistent storage:
```python
# In database.py
import os

# Use persistent disk if available, otherwise fallback to local
DATABASE_DIR = os.getenv("DATABASE_PATH", ".")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_DIR}/lottery_results.db"
```

#### 4. **Deploy to Render**
1. Push code to GitHub
2. Go to https://render.com
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Configure:
   - **Name**: lottery-scraper-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Plan**: Free
6. Click "Create Web Service"

#### 5. **Add Persistent Disk** (Optional but recommended):
1. In your service dashboard, go to "Disks"
2. Click "Add Disk"
3. **Name**: lottery-data
4. **Mount Path**: `/data`
5. **Size**: 1 GB (Free)
6. Update `DATABASE_PATH` env var to `/data`

### Files to Modify for Render

**`requirements.txt`** - Add gunicorn:
```txt
fastapi==0.128.0
uvicorn[standard]==0.32.1
beautifulsoup4==4.14.3
requests==2.32.5
sqlalchemy==2.0.45
apscheduler==3.11.0
python-multipart==0.0.20
gunicorn==21.2.0
```

**`main.py`** - Update port binding:
```python
import os

if __name__ == "__main__":
    # Use PORT env variable from Render
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

**`database.py`** - Use persistent disk:
```python
import os

# Use persistent disk path if available
DATABASE_DIR = os.getenv("DATABASE_PATH", ".")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_DIR}/lottery_results.db"
```

### Render Free Tier Limitations
- **Sleep after 15 min inactivity** - First request after sleep takes 30-60s
- **750 hours/month** - Enough for 24/7 if you don't exceed
- **Build time limit**: 15 minutes
- **PostgreSQL free tier**: 90 days (then auto-renews for another 90 days)

### Keep Service Awake (Optional)
Use a free cron service to ping your API every 10 minutes:

**UptimeRobot.com** (Free):
1. Create account
2. Add monitor: `https://your-app.onrender.com/api/health`
3. Interval: Every 5 minutes
4. Notification: Email

---

## Option 2: Railway.app

### Why Railway?
- ✅ **Free Trial**: $5 credit (lasts ~1 month)
- ✅ **PostgreSQL included**
- ✅ **No sleep** - Always running
- ✅ **Faster cold starts**
- ❌ **Not truly free** - Need credit card after trial

### Deployment Steps

#### 1. **Prepare Code**
Create `Procfile`:
```
web: python main.py
```

Create `railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python main.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### 2. **Deploy**
1. Go to https://railway.app
2. Click "Start a New Project"
3. Choose "Deploy from GitHub repo"
4. Select your repo
5. Add environment variables:
   - `PYTHON_VERSION`: 3.11
   - `PORT`: 8000
6. Railway auto-detects Python and deploys

#### 3. **Add PostgreSQL** (Optional):
1. In your project, click "New" → "Database" → "PostgreSQL"
2. Railway provides `DATABASE_URL` automatically
3. Update your code to use PostgreSQL instead of SQLite

### Railway Free Tier
- **$5 credit** (lasts ~1 month for small apps)
- **500 hours/month** after credit runs out (requires credit card)
- **No automatic sleep**

---

## Option 3: PythonAnywhere

### Why PythonAnywhere?
- ✅ **True free tier** - No credit card required
- ✅ **Persistent storage** - SQLite works perfectly
- ✅ **Always on** - No sleep
- ✅ **Scheduled tasks** - Free cron jobs
- ❌ **Limited outbound connections** - Can't scrape external sites easily
- ❌ **Whitelist required** - Only approved domains

### ⚠️ Major Issue: Scraping Limitations
**PythonAnywhere free tier only allows outbound connections to whitelisted sites.**
- `dlb.lk` - NOT on whitelist ❌
- `nlb.lk` - NOT on whitelist ❌

**This means you CANNOT scrape the lottery sites from free PythonAnywhere.**

**Workaround**: Use Paid tier ($5/month) to enable all outbound connections.

---

## Option 4: Fly.io

### Why Fly.io?
- ✅ **Free allowance**: 3 VMs with 256MB RAM
- ✅ **PostgreSQL free tier**
- ✅ **Always on**
- ✅ **Fast performance**
- ⚠️ Requires credit card for verification

### Deployment Steps

#### 1. **Install Fly CLI**
```powershell
pwsh -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

#### 2. **Login**
```bash
fly auth login
```

#### 3. **Create `fly.toml`**
```toml
app = "lottery-scraper-api"
primary_region = "sin"  # Singapore (closest to Sri Lanka)

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8000"
  PYTHON_VERSION = "3.11"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = false
  auto_start_machines = true
  min_machines_running = 1

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256
```

#### 4. **Deploy**
```bash
fly launch
fly deploy
```

### Fly.io Free Tier
- **3 shared-cpu VMs** (256MB RAM each)
- **3GB persistent storage**
- **160GB outbound transfer/month**
- **Requires credit card** for verification

---

## Option 5: Heroku

### Why Heroku?
- ✅ **Simple deployment**
- ✅ **Well documented**
- ❌ **No free tier anymore** - $5-7/month minimum
- ❌ **Sleeps after 30 min** (on Eco tier)

**Not recommended** due to paid tier requirement.

---

## Comparison Table

| Platform | Free Tier | Database | Sleep | Scraping | Persistent Storage | Credit Card |
|----------|-----------|----------|-------|----------|-------------------|-------------|
| **Render** ⭐ | ✅ 750h/mo | SQLite/PostgreSQL | 15min | ✅ | ✅ (with disk) | No |
| Railway | $5 credit | PostgreSQL | No | ✅ | ✅ | Yes (after trial) |
| PythonAnywhere | ✅ True | SQLite | No | ❌ Whitelist | ✅ | No |
| Fly.io | ✅ 3 VMs | PostgreSQL | No | ✅ | ✅ 3GB | Yes (verify) |
| Heroku | ❌ Paid | PostgreSQL | 30min | ✅ | ❌ | Yes |

---

## RECOMMENDED: Render.com Setup Guide

### Step-by-Step Complete Setup

#### 1. **Update Your Code**

**File: `main.py`**
```python
import os
import uvicorn
from fastapi import FastAPI
from api import app
from scheduler import start_scheduler

if __name__ == "__main__":
    # Start the scheduler for automatic scraping
    start_scheduler()
    
    # Get port from environment (Render sets this)
    port = int(os.getenv("PORT", 8000))
    
    # Run the API server
    uvicorn.run(app, host="0.0.0.0", port=port)
```

**File: `database.py`**
```python
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use persistent disk if DATABASE_PATH is set (Render disk mount)
DATABASE_DIR = os.getenv("DATABASE_PATH", ".")
DATABASE_FILE = "lottery_results.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_DIR}/{DATABASE_FILE}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

**File: `requirements.txt`**
```txt
fastapi==0.128.0
uvicorn[standard]==0.32.1
beautifulsoup4==4.14.3
requests==2.32.5
sqlalchemy==2.0.45
apscheduler==3.11.0
python-multipart==0.0.20
```

**File: `render.yaml`** (Create new)
```yaml
services:
  - type: web
    name: lottery-scraper-api
    runtime: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python main.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: PORT
        value: 8000
    healthCheckPath: /api/health
```

#### 2. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit with Render config"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/lottery-scraper-api.git
git push -u origin main
```

#### 3. **Deploy on Render**
1. Go to https://dashboard.render.com/
2. Click "New +" → "Web Service"
3. Connect GitHub account
4. Select your `lottery-scraper-api` repository
5. Render auto-detects settings from `render.yaml`
6. Click "Create Web Service"
7. Wait for build (~3-5 minutes)
8. Your API will be live at `https://lottery-scraper-api.onrender.com`

#### 4. **Add Persistent Disk** (Recommended)
1. In service dashboard, click "Disks" tab
2. Click "Add Disk"
3. **Name**: lottery-data
4. **Mount Path**: `/data`
5. **Size**: 1 GB
6. Click "Save"
7. Go to "Environment" tab
8. Add variable: `DATABASE_PATH` = `/data`
9. Redeploy (automatically triggers)

#### 5. **Test Your Deployment**
```bash
# Check health
curl https://lottery-scraper-api.onrender.com/api/health

# Get stats
curl https://lottery-scraper-api.onrender.com/api/stats

# View results
curl https://lottery-scraper-api.onrender.com/api/results/latest
```

#### 6. **Update `results-viewer.html`**
Change API base URL:
```javascript
const API_BASE = 'https://lottery-scraper-api.onrender.com';  // Your Render URL
```

#### 7. **Set Up UptimeRobot** (Keep alive)
1. Go to https://uptimerobot.com
2. Sign up (free)
3. Click "Add New Monitor"
4. **Monitor Type**: HTTP(s)
5. **Friendly Name**: Lottery API
6. **URL**: `https://lottery-scraper-api.onrender.com/api/health`
7. **Monitoring Interval**: 5 minutes
8. Click "Create Monitor"

This pings your API every 5 minutes to prevent sleep.

---

## Alternative: Using PostgreSQL on Render

If you want a proper database instead of SQLite:

### 1. **Add PostgreSQL to Render**
1. In Render dashboard, click "New +" → "PostgreSQL"
2. **Name**: lottery-db
3. **Plan**: Free
4. Click "Create Database"
5. Copy the "Internal Database URL"

### 2. **Update `requirements.txt`**
```txt
fastapi==0.128.0
uvicorn[standard]==0.32.1
beautifulsoup4==4.14.3
requests==2.32.5
sqlalchemy==2.0.45
apscheduler==3.11.0
python-multipart==0.0.20
psycopg2-binary==2.9.9  # PostgreSQL adapter
```

### 3. **Update `database.py`**
```python
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use PostgreSQL if DATABASE_URL is set, otherwise SQLite
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # PostgreSQL (Render)
    SQLALCHEMY_DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
else:
    # SQLite (local development)
    SQLALCHEMY_DATABASE_URL = "sqlite:///./lottery_results.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### 4. **Link Database to Web Service**
1. In your web service, go to "Environment" tab
2. Add environment variable:
   - **Key**: `DATABASE_URL`
   - **Value**: (paste the PostgreSQL Internal Database URL)
3. Save and redeploy

---

## Cost Estimate

### Render Free Tier
- **Web Service**: FREE (750 hours/month, sleeps after 15min)
- **PostgreSQL**: FREE for 90 days, then renews for another 90 days
- **Persistent Disk**: FREE 1GB
- **Total**: **$0/month**

### Railway (After trial)
- **Web Service**: ~$5/month
- **PostgreSQL**: Included
- **Total**: **~$5/month**

### Fly.io
- **Web Service**: FREE (3 VMs, 256MB each)
- **PostgreSQL**: FREE tier available
- **Total**: **$0/month** (requires credit card for verification)

---

## Final Recommendation

**For Your Use Case (Lottery Scraper):**

1. **Best Free Option**: **Render.com**
   - No credit card required
   - Includes database
   - Persistent storage
   - Easy deployment
   - Use UptimeRobot to prevent sleep

2. **If You Can Pay $5/Month**: **Railway.app**
   - Faster
   - No sleep
   - Better performance
   - Simpler management

3. **For Production (Future)**: **Fly.io** or **DigitalOcean App Platform**
   - Better uptime
   - More resources
   - Professional SLA

---

## Deployment Checklist

- [ ] Update `main.py` with PORT environment variable
- [ ] Update `database.py` with DATABASE_PATH support
- [ ] Add `render.yaml` configuration file
- [ ] Push code to GitHub
- [ ] Create Render account
- [ ] Deploy web service on Render
- [ ] Add persistent disk (optional but recommended)
- [ ] Set DATABASE_PATH environment variable
- [ ] Test API endpoints
- [ ] Update `results-viewer.html` with deployed URL
- [ ] Set up UptimeRobot monitoring (optional)
- [ ] Run historical backfill if needed

---

**Ready to deploy?** Follow the Render.com setup guide above! 🚀
