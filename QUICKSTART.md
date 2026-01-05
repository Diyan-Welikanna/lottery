# Quick Start Guide

## Step 1: Install Dependencies

```bash
cd lottery-scraper-api
pip install -r requirements.txt
```

## Step 2: Test the Scraper (Recommended First)

This will fetch data from both websites and show you what it finds:

```bash
python test_scraper.py
```

This will:
- Fetch from DLB and NLB websites
- Save HTML to `dlb_debug.html` and `nlb_debug.html` for inspection
- Show extracted results
- Ask if you want to save to database

To auto-save results:
```bash
python test_scraper.py --save
```

## Step 3: Inspect Debug Files (If Needed)

If the scraper doesn't find results correctly:
1. Open `dlb_debug.html` in a browser
2. Right-click → Inspect Element
3. Find the actual CSS classes for lottery results
4. Update `scraper.py` with correct selectors

## Step 4: Start the API Server

```bash
python main.py
```

The server will:
- Start on http://localhost:8000
- Run initial scrape
- Auto-scrape every 30 minutes
- Provide API endpoints

## Step 5: Test the API

Visit http://localhost:8000/docs for interactive API documentation

Or test with PowerShell:

```powershell
# Get latest results
Invoke-RestMethod -Uri "http://localhost:8000/api/results/latest"

# Get DLB results only
Invoke-RestMethod -Uri "http://localhost:8000/api/results/latest?board=DLB"

# Verify a ticket
$body = @{
    lottery_name = "sasiri"
    ticket_numbers = @("14", "27", "42")
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/verify" -Method POST -Body $body -ContentType "application/json"
```

## What's Improved

### DLB Scraper ✅
- Multiple parsing strategies (structured HTML, text patterns, scripts)
- Handles all DLB lotteries: Sasiri, Kapruka, Shanida, Super Ball, Ada Kotipathi, etc.
- Robust date parsing
- Debug mode to save HTML for inspection

### NLB Scraper ✅
- Table parsing (NLB often uses tables)
- Card/div parsing
- Text pattern matching
- Handles NLB lotteries: Mahajana Sampatha, Vasana Sampatha, Govisetha, etc.
- Debug mode enabled

### Features
- **3 parsing strategies** per scraper (tries multiple methods)
- **Debug mode** - saves HTML and shows detailed parsing info
- **Better error handling** - continues even if one strategy fails
- **More lottery types** - 8 DLB + 9 NLB lotteries in database
- **Flexible matching** - works even if HTML structure changes slightly

## Troubleshooting

### No results found?
1. Run `python test_scraper.py` to debug
2. Check `dlb_debug.html` and `nlb_debug.html`
3. Update CSS selectors in `scraper.py` based on actual HTML

### Connection errors?
- Check internet connection
- Verify websites are accessible: https://www.dlb.lk/result/en
- Try adding delay between requests

### Wrong data extracted?
- Enable debug mode: `python scraper.py --debug`
- Inspect what's being parsed
- Adjust regex patterns or selectors

## File Overview

- `test_scraper.py` - **START HERE** - Test and debug scraper
- `scraper.py` - Web scraping logic (improved with 3 strategies)
- `main.py` - Run API server with auto-scraping
- `api.py` - REST API endpoints
- `database.py` - Database models (now includes all lottery types)
