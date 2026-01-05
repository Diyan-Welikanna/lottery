# Deploy Lottery Scraper API to Render.com

## Prerequisites
- GitHub account with your lottery repository
- Render.com account (free tier available)

## Step 1: Prepare Your Repository

Your repository is already configured! The following files enable Render deployment:
- ✅ `render.yaml` - Render configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `main.py` - Uses PORT environment variable
- ✅ `database.py` - Uses DATABASE_URL environment variable
- ✅ `auth.py` - Optional API key authentication

## Step 2: Deploy to Render.com

### Option A: Deploy via Render Dashboard (Recommended)

1. **Go to Render.com**
   - Visit https://render.com
   - Sign up or log in with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `Diyan-Welikanna/lottery`
   - Render will auto-detect `render.yaml`

3. **Configure Service**
   - Name: `lottery-scraper-api`
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`

4. **Add Environment Variables** (in Render dashboard)
   ```
   PORT=8000
   DATABASE_PATH=/opt/render/project/data/lottery_results.db
   API_KEY=your-secret-api-key-here-change-this
   ```

5. **Add Persistent Disk** (Important!)
   - In your service settings → "Disks"
   - Click "Add Disk"
   - Name: `lottery-data`
   - Mount Path: `/opt/render/project/data`
   - Size: 1 GB (free tier)
   - This ensures your database persists across deployments

6. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy automatically
   - Wait 5-10 minutes for first deployment

### Option B: Deploy via render.yaml (Automatic)

If `render.yaml` is detected, Render auto-configures everything except environment variables.

You still need to manually add these in the dashboard:
- `API_KEY` (required for authentication)
- `DATABASE_PATH` (already in render.yaml)

## Step 3: Get Your API URL

After deployment succeeds:
- Your API URL: `https://lottery-scraper-api.onrender.com`
- API Docs: `https://lottery-scraper-api.onrender.com/docs`

## Step 4: Test Your Deployed API

### Without Authentication (if API_KEY not set)
```bash
curl https://lottery-scraper-api.onrender.com/api/stats
```

### With Authentication (recommended)
```bash
curl -H "X-API-Key: your-secret-api-key-here" \
  https://lottery-scraper-api.onrender.com/api/stats
```

## Authentication Setup

### Enable API Key Authentication

1. **Set API_KEY in Render Dashboard**
   - Go to Environment tab
   - Add: `API_KEY=MySecretKey123!ChangeThis`
   - Redeploy

2. **API Key is Now Required**
   - All requests need `X-API-Key` header
   - Without it: `403 Forbidden`

### Disable Authentication (Open API)

1. **Remove API_KEY**
   - Delete `API_KEY` environment variable
   - Redeploy
   - API is now public (no authentication)

## Important Notes

### Free Tier Limitations
- **Service sleeps after 15 minutes** of inactivity
- First request after sleep: ~30 seconds cold start
- **750 hours/month free** (enough for 24/7 if you only have 1 service)

### Keep Service Awake (Optional)
Use UptimeRobot (free) to ping your API every 5 minutes:
1. Sign up at https://uptimerobot.com
2. Add monitor: `https://lottery-scraper-api.onrender.com/`
3. Interval: 5 minutes
4. This prevents sleep during active hours

### Database Persistence
- **CRITICAL**: Add persistent disk (Step 2.5)
- Without disk: database resets on every deploy
- With disk: data survives deployments

### Scheduler Behavior
- Scraper runs every 60 minutes automatically
- Optimized for DLB results window (10 PM - 6 AM)
- Logs visible in Render dashboard

## Monitoring & Logs

### View Logs
- Render Dashboard → Your Service → "Logs" tab
- Real-time scraper activity and errors
- Filter by date/time

### Check Health
```bash
curl https://lottery-scraper-api.onrender.com/
```

Expected response:
```json
{
  "status": "online",
  "message": "Sri Lankan Lottery Results API",
  "version": "1.0.0"
}
```

## Updating Your Deployment

### Automatic Deployment (Recommended)
1. Push changes to GitHub `main` branch
2. Render auto-deploys within 2-5 minutes
3. Zero downtime deployment

### Manual Deployment
- Render Dashboard → "Manual Deploy" → "Deploy latest commit"

## Troubleshooting

### Service Won't Start
- Check logs for Python errors
- Verify `requirements.txt` has all dependencies
- Ensure `PORT` environment variable is set

### Database Empty After Deploy
- Add persistent disk (see Step 2.5)
- Verify `DATABASE_PATH=/opt/render/project/data/lottery_results.db`

### 403 Forbidden Errors
- Check if `API_KEY` is set
- Verify `X-API-Key` header in requests
- Remove `API_KEY` to disable authentication

### Scraper Not Running
- Check logs for errors
- Verify network access to nlb.lk and dlb.lk
- Trigger manual scrape: `POST /api/scrape`

## Cost Estimate

### Free Tier (What You Get)
- 750 hours/month web service
- 1 GB persistent disk
- Automatic HTTPS
- Auto-deploy from GitHub
- Custom domain support

### If You Exceed Free Tier
- $7/month for 24/7 uptime (unlimited hours)
- Additional disk: $1/GB/month

## Alternative Free Hosts

If Render doesn't work:
1. **Railway.app** - $5 trial credit, similar setup
2. **Fly.io** - 3 free VMs, more complex setup
3. **PythonAnywhere** - Free tier, but can't scrape external sites

## Next Steps

1. ✅ Deploy to Render (follow steps above)
2. ✅ Set API_KEY environment variable
3. ✅ Add persistent disk
4. ✅ Test API endpoints
5. ✅ Integrate with your OCR software (see integration guide below)

---

**Need help?** Check Render documentation: https://render.com/docs
