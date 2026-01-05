"""
Test script to debug and inspect lottery websites
Run this to see what the scraper finds and save HTML for manual inspection
"""

import sys
from scraper import DLBScraper, NLBScraper
from database import init_db

def test_dlb():
    """Test DLB scraper"""
    print("\n" + "="*70)
    print("TESTING DLB SCRAPER (Development Lotteries Board)")
    print("="*70)
    
    scraper = DLBScraper(debug=True)
    results = scraper.scrape_latest_results()
    
    print(f"\n📊 Found {len(results)} results from DLB")
    
    if results:
        print("\n✅ Sample Results:")
        for i, result in enumerate(results[:5], 1):
            print(f"\n  Result {i}:")
            print(f"    Lottery: {result['lottery_name']}")
            print(f"    Draw #: {result['draw_number']}")
            print(f"    Date: {result['draw_date']}")
            print(f"    Numbers: {result['winning_numbers']}")
            print(f"    Prize: {result['prize_amount']}")
    else:
        print("\n❌ No results found!")
        print("   Check dlb_debug.html to inspect the actual HTML structure")
    
    return results


def test_nlb():
    """Test NLB scraper"""
    print("\n" + "="*70)
    print("TESTING NLB SCRAPER (National Lotteries Board)")
    print("="*70)
    
    scraper = NLBScraper(debug=True)
    results = scraper.scrape_latest_results()
    
    print(f"\n📊 Found {len(results)} results from NLB")
    
    if results:
        print("\n✅ Sample Results:")
        for i, result in enumerate(results[:5], 1):
            print(f"\n  Result {i}:")
            print(f"    Lottery: {result['lottery_name']}")
            print(f"    Draw #: {result['draw_number']}")
            print(f"    Date: {result['draw_date']}")
            print(f"    Numbers: {result['winning_numbers']}")
            print(f"    Prize: {result['prize_amount']}")
    else:
        print("\n❌ No results found!")
        print("   Check nlb_debug.html to inspect the actual HTML structure")
    
    return results


def save_to_database(dlb_results, nlb_results):
    """Save results to database"""
    print("\n" + "="*70)
    print("SAVING TO DATABASE")
    print("="*70)
    
    # Initialize database
    init_db()
    
    # Save DLB results
    if dlb_results:
        dlb_scraper = DLBScraper()
        dlb_saved = dlb_scraper.save_results(dlb_results)
        print(f"✓ Saved {dlb_saved} DLB results to database")
    
    # Save NLB results
    if nlb_results:
        nlb_scraper = NLBScraper()
        nlb_saved = nlb_scraper.save_results(nlb_results)
        print(f"✓ Saved {nlb_saved} NLB results to database")


def main():
    print("\n🎰 Sri Lankan Lottery Scraper - Test Mode")
    print("This will:")
    print("  1. Fetch data from DLB and NLB websites")
    print("  2. Save HTML to dlb_debug.html and nlb_debug.html")
    print("  3. Show what data was extracted")
    print("  4. Optionally save to database")
    
    # Test DLB
    dlb_results = test_dlb()
    
    # Test NLB
    nlb_results = test_nlb()
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"DLB Results: {len(dlb_results)}")
    print(f"NLB Results: {len(nlb_results)}")
    
    if dlb_results or nlb_results:
        print("\n📁 Debug files created:")
        if dlb_results:
            print("  - dlb_debug.html (inspect this to see DLB website structure)")
        if nlb_results:
            print("  - nlb_debug.html (inspect this to see NLB website structure)")
        
        # Ask to save to database
        print("\n💾 Save these results to database? (y/n): ", end='')
        if '--save' in sys.argv or input().lower().strip() == 'y':
            save_to_database(dlb_results, nlb_results)
            print("\n✅ Results saved! You can now start the API server.")
        else:
            print("\nℹ️  Results not saved. Run with --save flag to auto-save.")
    else:
        print("\n⚠️  No results found from either website!")
        print("   This could mean:")
        print("   1. The websites are down")
        print("   2. The HTML structure has changed")
        print("   3. Network/firewall blocking the requests")
        print("\n   Check the debug HTML files to investigate.")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
