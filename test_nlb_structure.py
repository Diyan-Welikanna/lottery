"""
Test script to analyze NLB lottery result page structure
This will help us understand the HTML and build proper scrapers
"""

import requests
from bs4 import BeautifulSoup
import json

# NLB lottery configurations with their Jan 1 draw numbers
NLB_LOTTERIES = {
    'suba-dawasak': {'jan1_draw': 177, 'display_name': 'SUBA DAWASAK'},
    'nlb-jaya': {'jan1_draw': 329, 'display_name': 'NLB JAYA'},
    'ada-sampatha': {'jan1_draw': 636, 'display_name': 'ADA SAMPATHA'},
    'handahana': {'jan1_draw': 1370, 'display_name': 'HANDAHANA'},
    'dhana-nidhanaya': {'jan1_draw': 2091, 'display_name': 'DHANA NIDHANAYA'},
    'mega-power': {'jan1_draw': 2409, 'display_name': 'MEGA POWER'},
    'govisetha': {'jan1_draw': 4303, 'display_name': 'GOVISETHA'},
    'mahajana-sampatha': {'jan1_draw': 6061, 'display_name': 'MAHAJANA SAMPATHA'},
}

def test_nlb_page(lottery_slug, draw_number):
    """Fetch and analyze a single NLB lottery result page"""
    url = f"https://www.nlb.lk/results/{lottery_slug}/{draw_number}"
    
    print(f"\n{'='*70}")
    print(f"Testing: {lottery_slug.upper()} - Draw #{draw_number}")
    print(f"URL: {url}")
    print('='*70)
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
        }
        
        # Use session to maintain cookies
        session = requests.Session()
        
        # First request will set the cookie
        response = session.get(url, headers=headers, timeout=10)
        
        # Check if we got a cookie-setting page
        if 'setCookie' in response.text and 'location.reload' in response.text:
            print("  Cookie protection detected!")
            
            # Extract the cookie value from the JavaScript
            import re
            import time
            
            cookie_match = re.search(r"setCookie\('([^']+)','([^']+)',", response.text)
            if cookie_match:
                cookie_name = cookie_match.group(1)
                cookie_value = cookie_match.group(2)
                print(f"  Setting cookie: {cookie_name}={cookie_value[:20]}...")
                
                # Set the cookie manually
                session.cookies.set(cookie_name, cookie_value, domain='.nlb.lk', path='/')
            
            # Wait a bit then make second request
            time.sleep(3)
            print("  Making second request with cookie...")
            
            # Make the second request with all headers
            response = session.get(url, headers=headers, timeout=15)
            print(f"  Second response size: {len(response.text)} bytes")
        
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Save HTML for manual inspection
        filename = f'nlb_{lottery_slug}_{draw_number}_debug.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print(f"✓ HTML saved to: {filename}")
        
        # Try to extract information
        print("\n--- Analyzing Page Structure ---")
        
        # Look for draw number
        draw_elements = soup.find_all(string=lambda text: text and 'draw' in text.lower())
        if draw_elements:
            print(f"\nDraw mentions found: {len(draw_elements)}")
            for elem in draw_elements[:3]:
                print(f"  - {elem.strip()[:100]}")
        
        # Look for dates
        date_patterns = soup.find_all(string=lambda text: text and '2026' in text)
        if date_patterns:
            print(f"\nDate mentions found: {len(date_patterns)}")
            for elem in date_patterns[:3]:
                print(f"  - {elem.strip()[:100]}")
        
        # Look for numbers (potential winning numbers)
        # Find all text that contains only 1-2 digits
        import re
        numbers = []
        for text in soup.stripped_strings:
            if re.match(r'^\d{1,2}$', text):
                numbers.append(text)
        
        if numbers:
            print(f"\nPotential winning numbers found: {numbers[:15]}")
        
        # Look for common containers
        print("\n--- Common Elements ---")
        result_divs = soup.find_all('div', class_=re.compile(r'result|lottery|draw', re.I))
        print(f"Result-related divs: {len(result_divs)}")
        
        tables = soup.find_all('table')
        print(f"Tables found: {len(tables)}")
        
        # Print page title
        title = soup.find('title')
        if title:
            print(f"\nPage title: {title.text.strip()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("="*70)
    print("NLB LOTTERY PAGE STRUCTURE ANALYZER")
    print("="*70)
    print("\nThis will fetch sample pages and save HTML for inspection")
    print("We'll test the first draw (Jan 1) for each lottery\n")
    
    results = {}
    
    # Test first 3 lotteries to understand structure
    test_lotteries = ['suba-dawasak', 'mahajana-sampatha', 'govisetha']
    
    for lottery_slug in test_lotteries:
        lottery_info = NLB_LOTTERIES[lottery_slug]
        draw_num = lottery_info['jan1_draw']
        
        success = test_nlb_page(lottery_slug, draw_num)
        results[lottery_slug] = success
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    for lottery, success in results.items():
        status = "✓ SUCCESS" if success else "❌ FAILED"
        print(f"{lottery}: {status}")
    
    print("\n" + "="*70)
    print("Next Steps:")
    print("1. Open the generated *_debug.html files in a browser")
    print("2. Inspect the HTML structure to find:")
    print("   - Where the draw number is displayed")
    print("   - Where the winning numbers are shown")
    print("   - Where the draw date is located")
    print("   - Any prize information")
    print("3. Update the NLB scraper with the correct selectors")
    print("="*70)

if __name__ == "__main__":
    main()
