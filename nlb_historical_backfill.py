"""
NLB Historical Backfill Script
Scrape NLB lottery results from January 1st to today using individual draw URLs
"""

from datetime import datetime
import time
from scraper import NLBScraper
from database import SessionLocal, LotteryResult

# NLB lottery configurations with their Jan 1, 2026 draw numbers
NLB_LOTTERIES = {
    'suba-dawasak': {
        'jan1_draw': 177,
        'display_name': 'SUBA DAWASAK',
        'draws_per_day': 1  # Approximate draws per day
    },
    'nlb-jaya': {
        'jan1_draw': 329,
        'display_name': 'NLB JAYA',
        'draws_per_day': 1
    },
    'ada-sampatha': {
        'jan1_draw': 636,
        'display_name': 'ADA SAMPATHA',
        'draws_per_day': 1
    },
    'handahana': {
        'jan1_draw': 1370,
        'display_name': 'HANDAHANA',
        'draws_per_day': 1
    },
    'dhana-nidhanaya': {
        'jan1_draw': 2091,
        'display_name': 'DHANA NIDHANAYA',
        'draws_per_day': 1
    },
    'mega-power': {
        'jan1_draw': 2409,
        'display_name': 'MEGA POWER',
        'draws_per_day': 1
    },
    'govisetha': {
        'jan1_draw': 4303,
        'display_name': 'GOVISETHA',
        'draws_per_day': 1
    },
    'mahajana-sampatha': {
        'jan1_draw': 6061,
        'display_name': 'MAHAJANA SAMPATHA',
        'draws_per_day': 1
    },
}


def calculate_draws_to_scrape():
    """Calculate how many draws to scrape based on days since Jan 1"""
    jan1 = datetime(2026, 1, 1)
    today = datetime.now()
    days_since_jan1 = (today - jan1).days
    
    # Add 1 to include today (Jan 4 = 4 days = draws 0,1,2,3)
    return days_since_jan1 + 1


def scrape_historical_nlb(debug=False, delay_seconds=4):
    """
    Scrape NLB lottery results from January 1st to today
    
    Args:
        debug: Enable debug mode
        delay_seconds: Delay between requests to avoid rate limiting
    """
    print("=" * 70)
    print("NLB HISTORICAL BACKFILL - January 1st to Today")
    print("=" * 70)
    print(f"Start time: {datetime.now()}")
    
    # Calculate draws to scrape
    draws_to_scrape = calculate_draws_to_scrape()
    print(f"\nDays since Jan 1: {draws_to_scrape}")
    print(f"Will scrape {draws_to_scrape} draw(s) for each lottery\n")
    
    scraper = NLBScraper(debug=debug)
    db = SessionLocal()
    
    total_scraped = 0
    total_saved = 0
    total_failed = 0
    
    try:
        for lottery_slug, lottery_info in NLB_LOTTERIES.items():
            print(f"\n{'='*70}")
            print(f"Lottery: {lottery_info['display_name']} ({lottery_slug})")
            print(f"Starting from draw #{lottery_info['jan1_draw']}")
            print(f"{'='*70}")
            
            start_draw = lottery_info['jan1_draw']
            
            for offset in range(draws_to_scrape):
                current_draw = start_draw + offset
                
                # Check if already in database
                existing = db.query(LotteryResult).filter(
                    LotteryResult.lottery_name == lottery_slug.replace('-', '_'),
                    LotteryResult.draw_number == str(current_draw)
                ).first()
                
                if existing:
                    print(f"  Draw #{current_draw}: ⏭️  Already in database, skipping")
                    continue
                
                # Scrape the draw
                result = scraper.scrape_individual_draw(lottery_slug, current_draw)
                
                if result:
                    # Save to database
                    try:
                        lottery_result = LotteryResult(
                            lottery_name=result['lottery_name'],
                            draw_number=result['draw_number'],
                            draw_date=result['draw_date'],
                            winning_numbers=result['winning_numbers'],
                            prize_amount=result.get('prize_amount'),
                            additional_data=result.get('additional_data', {})
                        )
                        db.add(lottery_result)
                        db.commit()
                        
                        print(f"  Draw #{current_draw}: ✅ Scraped and saved - Numbers: {result['winning_numbers']}")
                        total_saved += 1
                    except Exception as e:
                        print(f"  Draw #{current_draw}: ❌ Failed to save - {e}")
                        db.rollback()
                        total_failed += 1
                else:
                    print(f"  Draw #{current_draw}: ❌ Scraping failed")
                    total_failed += 1
                
                total_scraped += 1
                
                # Delay to avoid rate limiting
                if offset < draws_to_scrape - 1:  # Don't delay after last draw
                    time.sleep(delay_seconds)
            
            print(f"\nCompleted {lottery_info['display_name']}")
            print(f"  Total attempts: {draws_to_scrape}")
            print(f"  Successful: {sum(1 for i in range(draws_to_scrape) if db.query(LotteryResult).filter(LotteryResult.lottery_name == lottery_slug.replace('-', '_'), LotteryResult.draw_number == str(start_draw + i)).first())}")
    
    finally:
        db.close()
    
    print("\n" + "=" * 70)
    print("BACKFILL SUMMARY")
    print("=" * 70)
    print(f"Total draws attempted: {total_scraped}")
    print(f"Successfully saved: {total_saved}")
    print(f"Failed: {total_failed}")
    print(f"End time: {datetime.now()}")
    print("=" * 70)


if __name__ == "__main__":
    import sys
    
    debug_mode = '--debug' in sys.argv
    
    print("🎯 Sri Lankan NLB Historical Lottery Scraper")
    print("📅 Target: January 1, 2026 to Today")
    print()
    
    if debug_mode:
        print("🔍 DEBUG MODE ENABLED - HTML files will be saved")
        print()
    
    # Ask for confirmation
    response = input("This will scrape all NLB lottery draws from Jan 1 to today. Continue? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        exit(0)
    
    scrape_historical_nlb(debug=debug_mode, delay_seconds=4)
