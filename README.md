# Sri Lankan Lottery Scraper API 🎰

A comprehensive FastAPI-based service that scrapes lottery results from both NLB (National Lotteries Board) and DLB (Development Lotteries Board) websites, featuring **advanced ball type categorization** for accurate ticket verification.

## ✨ Features

- 🎯 **Ball Type Categorization**: Identifies Letters, Zodiac Signs, Super Numbers, Regular Numbers, and Promotional balls
- 🔄 **Automatic Scraping**: Hourly scheduled scraping with intelligent retry logic
- 💾 **SQLite Database**: Persistent storage with structured JSON data
- 🚀 **REST API**: 9 comprehensive endpoints for accessing lottery data
- ✅ **Ticket Verification**: Match ticket numbers with ball type validation
- 📊 **Statistics Dashboard**: Real-time scraping stats and success rates
- 🌐 **Results Viewer**: Beautiful HTML interface with color-coded ball types
- 🔐 **Cookie Protection Handling**: Automatic bypass for NLB's JavaScript protection
- 📝 **Comprehensive Logging**: File-based logging with rotation

## 🎲 Supported Lotteries

### NLB (National Lotteries Board) - 8 Lotteries
1. **Suba Dawasak** - Zodiac + 3 Numbers + Promotional (4 numbers)
2. **Handahana** - Zodiac + 4 Numbers
3. **Mega Power** ⭐ - Letter + **Super Number** + 4 Numbers
4. **Ada Sampatha** - 9 Numbers + Letter
5. **Dhana Nidhanaya** - Letter + 4 Numbers
6. **Govisetha** - Letter + 4 Numbers
7. **NLB Jaya** - Letter + 4 Numbers
8. **Mahajana Sampatha** - Letter + 6 Numbers

### DLB (Development Lotteries Board) - 9 Lotteries
1. **Ada Kotipathi** - Letter + 4 Numbers
2. **Shanida** - Letter + 4 Numbers
3. **Lagna Wasana** - 4 Numbers
4. **Supiri Dhana Sampatha** - Letter + 6 Numbers
5. **Super Ball** - Letter + 4 Numbers
6. **Kapruka** - Letter + 5 Numbers
7. **Jayoda** - Letter + 4 Numbers
8. **Sasiri** - 3 Numbers
9. **Jaya Sampatha** - Letter + 4 Numbers

## 🏗️ Ball Type System

The scraper categorizes **5 distinct ball types**:

- **LETTER** (A-Z) - Blue circle - Used in 13 lotteries
- **ZODIAC** (ARIES, TAURUS, etc.) - Purple square - Used in 2 lotteries (Suba Dawasak, Handahana)
- **SUPER NUMBER** ⭐ - Red pulsing circle - Only in Mega Power
- **REGULAR NUMBER** - Purple gradient circle - All lotteries
- **PROMOTIONAL** - Green square - Only in Suba Dawasak bonus draw

Example response:
```json
{
  "lottery_name": "mega_power",
  "draw_number": "2409",
  "winning_numbers": [
    {"type": "letter", "value": "U"},
    {"type": "super", "value": "21"},
    {"type": "number", "value": "18"},
    {"type": "number", "value": "23"},
    {"type": "number", "value": "31"},
    {"type": "number", "value": "76"}
  ]
}
```

## Installation

### 1. Install Dependencies

```bash
cd lottery-scraper-api
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env`:

```bash
copy .env.example .env
```

Edit `.env` if needed:
```
DATABASE_URL=sqlite:///./lottery_results.db
SCRAPER_INTERVAL_MINUTES=30
API_HOST=0.0.0.0
API_PORT=8000
```

### 3. Run the Server

```bash
python main.py
```

The API will:
- Start on http://localhost:8000
- Run initial scrape immediately
- Schedule scraping every 30 minutes
- Initialize SQLite database

## 📚 Documentation

- **[Lottery Structure Guide](LOTTERY_STRUCTURE_GUIDE.md)** - Complete breakdown of DLB & NLB lottery structures, ball types, HTML patterns
- **[Hosting Guide](HOSTING_GUIDE.md)** - Deploy to Render, Railway, Fly.io, or PythonAnywhere (free options!)
- **[Ball Type Summary](BALL_TYPE_SUMMARY.md)** - Implementation details of ball categorization system

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/YOUR_USERNAME/lottery-scraper-api.git
cd lottery-scraper-api
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python main.py
```

The server will:
- Start on http://localhost:8000
- Run initial scrape immediately
- Schedule hourly scraping
- Initialize SQLite database

### 3. View Results

Open in browser:
- **API Docs**: http://localhost:8000/docs
- **Results Viewer**: http://localhost:8000/results-viewer.html
- **Stats**: http://localhost:8000/api/stats

## 📡 API Endpoints

### GET /api/lotteries
Get all lottery types with metadata.

**Response:**
```json
[
  {
    "name": "mega_power",
    "display_name": "Mega Power",
    "board": "NLB",
    "has_letters": true,
    "has_zodiac": false,
    "has_super": true
  }
]
```

### GET /api/results/latest?limit=10&board=DLB
Get latest lottery results.

**Parameters:**
- `limit` (optional): 1-100, default 10
- `board` (optional): DLB or NLB

**Response:**
```json
[
  {
    "lottery_name": "mega_power",
    "draw_number": "2409",
    "draw_date": "2026-01-05T00:00:00",
    "winning_numbers": [
      {"type": "letter", "value": "U"},
      {"type": "super", "value": "21"},
      {"type": "number", "value": "18"}
    ],
    "prize_amount": null,
    "scraped_at": "2026-01-05T12:37:21"
  }
]
```

### GET /api/results/{lottery_name}?limit=5
Get results for specific lottery.

### GET /api/results/date/{date}
Get all results for a specific date (format: YYYY-MM-DD).

### POST /api/verify
Verify ticket numbers against winning results.

**Request:**
```json
{
  "lottery_name": "mega_power",
  "ticket_numbers": [
    {"type": "letter", "value": "U"},
    {"type": "super", "value": "21"},
    {"type": "number", "value": "18"}
  ],
  "draw_number": "2409"
}
```

**Response:**
```json
{
  "is_winner": true,
  "matched_numbers": [
    {"type": "letter", "value": "U"},
    {"type": "super", "value": "21"},
    {"type": "number", "value": "18"}
  ],
  "match_count": 3,
  "total_numbers": 6
}
```

### POST /api/scrape
Manually trigger a scrape of all lottery websites.

### GET /api/stats
Get database and scraping statistics.

**Response:**
```json
{
  "total_results": 45,
  "total_lotteries": 17,
  "dlb_results": 9,
  "nlb_results": 36,
  "last_scrape": "2026-01-05T12:37:21",
  "database_size": "45 KB"
}
```

### GET /api/health
Health check endpoint (returns 200 OK).

## 📁 Project Structure

```
lottery-scraper-api/
├── main.py                       # Entry point - starts server + scheduler
├── api.py                        # FastAPI routes (9 endpoints)
├── scraper.py                    # Web scraping logic (DLB & NLB with ball types)
├── database.py                   # SQLAlchemy models and DB config
├── scheduler.py                  # APScheduler for hourly scraping
├── nlb_historical_backfill.py    # Backfill NLB from Jan 1st
├── results-viewer.html           # Beautiful results viewer UI
├── requirements.txt              # Python dependencies
├── lottery_results.db            # SQLite database (auto-created)
├── logs/
│   └── scraper.log              # Rotating log files
├── LOTTERY_STRUCTURE_GUIDE.md   # Complete lottery breakdown
├── HOSTING_GUIDE.md             # Free hosting options (Render, Railway, etc.)
├── BALL_TYPE_SUMMARY.md         # Ball type implementation details
└── README.md                    # This file
```

## 🗄️ Database Schema

### lottery_results Table
```python
{
  "id": 1,                                    # Primary key
  "lottery_name": "mega_power",               # Lottery identifier
  "draw_number": "2409",                      # Draw number
  "draw_date": "2026-01-05",                  # Draw date
  "winning_numbers": [                        # JSON array with ball types
    {"type": "letter", "value": "U"},
    {"type": "super", "value": "21"},
    {"type": "number", "value": "18"}
  ],
  "prize_amount": null,                       # Prize value (if available)
  "additional_data": {                        # Extra metadata
    "source_url": "https://...",
    "scrape_method": "individual_draw"
  },
  "scraped_at": "2026-01-05T12:37:21"        # Timestamp
}
```

## 🔧 Development

### Run Scraper Only (No API)
```bash
python scraper.py
```

### Run NLB Historical Backfill
```bash
python nlb_historical_backfill.py
```
Scrapes all NLB lotteries from January 1st to today.

### View Logs
```bash
cat logs/scraper.log
```

### Clear Database
```python
python -c "from database import SessionLocal, LotteryResult; db = SessionLocal(); db.query(LotteryResult).delete(); db.commit()"
```

## 🐛 Troubleshooting

### Results showing "[object Object]"
✅ **FIXED** - Updated `results-viewer.html` to properly display ball types with color coding.

### Scraper not finding NLB results
NLB requires individual draw scraping with cookie protection. Use `nlb_historical_backfill.py` to scrape specific draws.

### Database errors
```bash
# Delete and recreate database
del lottery_results.db
python main.py
```

### Port already in use
Change port when running:
```bash
python -c "import os; os.environ['PORT']='8001'; exec(open('main.py').read())"
```

### Logs too large
Logs auto-rotate at 10MB. Delete old logs:
```bash
del logs/scraper.log.*
```

## 🚀 Deployment

### Quick Deploy to Render (Free)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Render**:
   - Go to https://render.com
   - New Web Service → Connect GitHub repo
   - Auto-detects Python app
   - Click "Create Web Service"
   - Your API is live!

3. **Add Persistent Storage** (Optional):
   - In Render dashboard: Disks → Add Disk
   - Mount path: `/data`
   - Add env var: `DATABASE_PATH=/data`

See **[HOSTING_GUIDE.md](HOSTING_GUIDE.md)** for complete deployment instructions.

## 📖 Further Reading

- **[LOTTERY_STRUCTURE_GUIDE.md](LOTTERY_STRUCTURE_GUIDE.md)** - Detailed breakdown of all 17 lotteries, ball types, HTML structures, and scraping patterns
- **[HOSTING_GUIDE.md](HOSTING_GUIDE.md)** - Step-by-step guides for deploying to Render, Railway, Fly.io, and PythonAnywhere (all free options!)
- **[BALL_TYPE_SUMMARY.md](BALL_TYPE_SUMMARY.md)** - Technical implementation of ball type categorization system

## 🎯 Use Cases

- **Lottery Shops**: Display latest results in real-time
- **Mobile Apps**: API backend for lottery checking apps
- **Ticket Verification**: OCR + API verification system
- **Data Analysis**: Historical lottery data analysis
- **Notifications**: Alert users when specific numbers win

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## ⚖️ Legal & Disclaimer

This project is for **educational and personal use only**. Before commercial use:
- Check DLB/NLB terms of service
- Respect robots.txt and rate limiting
- Consider getting official API access
- Ensure compliance with Sri Lankan data protection laws

**Disclaimer**: This software is provided "as is" without warranty. The authors are not responsible for any misuse or legal issues arising from use of this software.

## 📧 Support

For issues or questions:
- Open a GitHub issue
- Check existing documentation
- Review logs for error details

---

**Made with ❤️ for Sri Lankan lottery enthusiasts**

**Project Status**: ✅ Production Ready
**Last Updated**: January 5, 2026
**Version**: 2.0 (with ball type categorization)
