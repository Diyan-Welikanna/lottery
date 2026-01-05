from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import os
from scraper import run_scraper

def scheduled_scrape():
    """Function to run on schedule"""
    print(f"\n{'='*50}")
    print(f"Scheduled scrape triggered at {datetime.now()}")
    print(f"{'='*50}")
    run_scraper()


def start_scheduler():
    """Start the background scheduler"""
    # Changed default from 30 to 60 minutes for hourly execution
    interval_minutes = int(os.getenv("SCRAPER_INTERVAL_MINUTES", 60))
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=scheduled_scrape,
        trigger=IntervalTrigger(minutes=interval_minutes),
        id='lottery_scraper',
        name='Scrape lottery results',
        replace_existing=True
    )
    
    scheduler.start()
    print(f"Scheduler started - will scrape every {interval_minutes} minutes")
    print(f"Optimized for DLB results window: 10 PM - 6 AM (8 hours)")
    
    # Run scraper immediately on startup
    print("Running initial scrape...")
    run_scraper()
    
    return scheduler
