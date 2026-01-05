import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import re
import json
import logging
import os
from database import SessionLocal, LotteryResult, LotteryType

# Setup logging
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'{log_dir}/scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DLBScraper:
    """Scraper for Development Lotteries Board (DLB) website"""
    
    def __init__(self, debug=False):
        self.base_url = "https://www.dlb.lk"
        self.results_url = f"{self.base_url}/result/en"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.debug = debug
    
    def scrape_latest_results(self) -> List[Dict]:
        """Scrape latest lottery results from DLB website"""
        try:
            logger.info(f"Fetching DLB results from: {self.results_url}")
            response = requests.get(self.results_url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            if self.debug:
                os.makedirs('dlb/misc', exist_ok=True)
                self._save_debug_html(soup, 'dlb/misc/dlb_debug.html')
            
            results = []
            
            # Strategy 1: Try to find result cards/containers using flexible regex (NOT hardcoded selectors)
            result_sections = soup.find_all('div', class_=re.compile(r'result|lottery|card|draw', re.I))
            
            if result_sections and self.debug:
                print(f"Found {len(result_sections)} potential result sections")
            
            # Strategy 2: Look for table rows
            if not result_sections:
                result_sections = soup.find_all('tr', class_=re.compile(r'result|row', re.I))
            
            # Strategy 3: Look for list items
            if not result_sections:
                result_sections = soup.find_all('li', class_=re.compile(r'result|lottery', re.I))
            
            # Parse each section
            for section in result_sections:
                result_data = self._parse_result_section(section)
                if result_data:
                    results.append(result_data)
            
            # Fallback: Parse from text patterns
            if not results:
                print("No structured results found. Trying text pattern matching...")
                results = self._parse_from_text(soup)
            
            # Additional: Try to find results in script tags (JSON data)
            if not results:
                results = self._parse_from_scripts(soup)
            
            logger.info(f"DLB: Found {len(results)} lottery results")
            return results
            
        except requests.RequestException as e:
            logger.error(f"Error fetching DLB results: {e}")
            return []
        except Exception as e:
            logger.error(f"Error parsing DLB results: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
            return []
    
    def _parse_result_section(self, section) -> Optional[Dict]:
        """Parse individual DLB result section using actual HTML structure"""
        try:
            # DLB Structure:
            # <h2 class="lot_m_re_heading">Ada Kotipathi</h2>
            # <h3 class="lot_m_re_date">Draw Number - 2864  |  2026-Jan-04 Sunday</h3>
            # <ul class="result_detail_result"><li><h6 class="eng_letter">Y</h6></li><li><h6 class="number_circle">08</h6></li>...
            
            # Find lottery name
            lottery_name_elem = section.find(['h2', 'h3', 'h4'], class_=re.compile(r'lot_m_re_heading|lottery.*name', re.I))
            if not lottery_name_elem:
                return None
            
            lottery_name = lottery_name_elem.get_text(strip=True)
            
            # Find draw number and date
            date_elem = section.find(['h3', 'h4', 'div'], class_=re.compile(r'lot_m_re_date|date', re.I))
            draw_num = None
            draw_date = datetime.now()
            
            if date_elem:
                date_text = date_elem.get_text(strip=True)
                # Extract draw number: "Draw Number - 2864  |  2026-Jan-04 Sunday"
                draw_match = re.search(r'Draw\s*Number\s*-\s*(\d+)', date_text, re.I)
                if draw_match:
                    draw_num = draw_match.group(1)
                
                # Extract date: "2026-Jan-04" or similar
                date_match = re.search(r'(\d{4}[-/]\w{3}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4}|\d{4}-\w+-\d{2})', date_text)
                if date_match:
                    draw_date = self._parse_date(date_match.group(1))
            
            # Find winning numbers in result_detail_result ul with ball type categorization
            winning_nums = []
            result_list = section.find('ul', class_=re.compile(r'result_detail_result', re.I))
            if result_list:
                # Find all list items with h6 tags (numbers, letters, zodiacs)
                number_items = result_list.find_all('li')
                for item in number_items:
                    h6 = item.find('h6')
                    if h6:
                        num_text = h6.get_text(strip=True)
                        if not num_text:
                            continue
                        
                        # Determine ball type based on CSS classes
                        h6_classes = h6.get('class', [])
                        ball_type = 'number'  # default
                        
                        if 'eng_letter' in h6_classes or 'lagna_letter' in h6_classes:
                            ball_type = 'letter'
                        elif 'zodiac' in ' '.join(h6_classes).lower():
                            ball_type = 'zodiac'
                        elif re.match(r'^[A-Z]$', num_text):
                            # Single uppercase letter (fallback detection)
                            ball_type = 'letter'
                        elif re.match(r'^\d{1,2}$', num_text):
                            # Number
                            ball_type = 'number'
                        elif len(num_text) > 2:
                            # Likely zodiac sign name (ARIES, TAURUS, etc.)
                            ball_type = 'zodiac'
                        
                        # Store as structured data
                        winning_nums.append({
                            "type": ball_type,
                            "value": num_text
                        })
            
            if lottery_name and winning_nums:
                logger.info(f"DLB: Parsed {lottery_name} - Draw #{draw_num}, Numbers: {winning_nums}")
                return {
                    'lottery_name': lottery_name.lower().replace(' ', '_'),
                    'draw_number': draw_num,
                    'draw_date': draw_date,
                    'winning_numbers': winning_nums,
                    'prize_amount': None
                }
                    
        except Exception as e:
            logger.error(f"Error parsing DLB section: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
        
        return None
    
    def _parse_from_text(self, soup) -> List[Dict]:
        """Fallback: Parse using text pattern matching for all DLB lotteries"""
        results = []
        text = soup.get_text()
        
        if self.debug:
            print("\n=== DLB TEXT PARSING ===")
        
        # Pattern for all DLB lottery types
        pattern = r'(SASIRI|KAPRUKA|SHANIDA|SUPER BALL|SUPER\s*BALL|ADA KOTIPATHI|ADA\s*KOTIPATHI|JAYA SAMPATHA|JAYA\s*SAMPATHA|LAGNA WASANA|LAGNA\s*WASANA|SUPIRI DHANA SAMPATHA|SUPIRI\s*DHANA\s*SAMPATHA)\s*-?\s*(\d+)?\s*\|?\s*([\d\-A-Z\s]+)?'
        matches = re.findall(pattern, text, re.IGNORECASE)
        
        if self.debug:
            print(f"Found {len(matches)} DLB lottery mentions")
        
        for match in matches:
            lottery_name, draw_number, date_str = match
            lottery_clean = lottery_name.strip()
            
            lottery_pos = text.find(lottery_name)
            if lottery_pos > -1:
                context = text[lottery_pos:lottery_pos + 200]
                number_matches = re.findall(r'\b(\d{1,2})\b', context)
                winning_nums = [n for n in number_matches if int(n) < 100][:10]
            else:
                winning_nums = []
            
            results.append({
                'lottery_name': lottery_clean.lower().replace(' ', '_'),
                'draw_number': draw_number if draw_number else None,
                'draw_date': self._parse_date(date_str) if date_str else datetime.now(),
                'winning_numbers': winning_nums,
                'prize_amount': None
            })
        
        return results
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse date string to datetime"""
        try:
            date_str = date_str.strip().upper()
            date_str = re.sub(r'(MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY)', '', date_str).strip()
            
            formats = ['%Y-%b-%d', '%Y-%m-%d', '%d-%b-%Y', '%d/%m/%Y', '%Y/%m/%d', '%d-%m-%Y', '%m/%d/%Y']
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            return datetime.now()
        except:
            return datetime.now()
    
    def _parse_from_scripts(self, soup) -> List[Dict]:
        """Try to extract lottery data from JavaScript/JSON"""
        results = []
        try:
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string:
                    json_match = re.search(r'\{[^{}]*lottery[^{}]*\}', script.string, re.I)
                    if json_match:
                        try:
                            data = json.loads(json_match.group(0))
                            if self.debug:
                                print("Found JSON data:", data)
                        except:
                            pass
        except:
            pass
        return results
    
    def _save_debug_html(self, soup, filename):
        """Save HTML for debugging"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            print(f"Debug HTML saved to {filename}")
        except:
            pass
    
    def save_results(self, results: List[Dict]) -> int:
        """Save results to database"""
        db = SessionLocal()
        saved_count = 0
        duplicate_count = 0
        
        try:
            for result in results:
                existing = db.query(LotteryResult).filter(
                    LotteryResult.lottery_name == result['lottery_name'],
                    LotteryResult.draw_number == result['draw_number']
                ).first()
                
                if not existing:
                    lottery_result = LotteryResult(
                        lottery_name=result['lottery_name'],
                        draw_number=result['draw_number'],
                        draw_date=result['draw_date'],
                        winning_numbers=result['winning_numbers'],
                        prize_amount=result.get('prize_amount'),
                        additional_data=result.get('additional_data', {})
                    )
                    db.add(lottery_result)
                    saved_count += 1
                    logger.info(f"DLB: Saved {result['lottery_name']} draw #{result['draw_number']}")
                else:
                    duplicate_count += 1
                    logger.debug(f"DLB: Duplicate skipped - {result['lottery_name']} draw #{result['draw_number']}")
            
            db.commit()
            if duplicate_count > 0:
                logger.info(f"DLB: Skipped {duplicate_count} duplicates")
            return saved_count
        except Exception as e:
            logger.error(f"Error saving DLB results: {e}")
            db.rollback()
            return 0
        finally:
            db.close()


class NLBScraper:
    """Scraper for National Lotteries Board (NLB) website"""
    
    def __init__(self, debug=False):
        self.base_url = "https://www.nlb.lk"
        self.results_url = f"{self.base_url}/English/results/"
        self.headers = {
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
        self.debug = debug
    
    def scrape_individual_draw(self, lottery_slug: str, draw_number: int) -> Optional[Dict]:
        """
        Scrape a specific NLB lottery draw using individual draw URL
        
        Args:
            lottery_slug: URL slug like 'suba-dawasak', 'govisetha', etc.
            draw_number: Draw number like 177, 4303, etc.
        
        Returns:
            Dict with lottery result data or None if failed
        """
        url = f"{self.base_url}/results/{lottery_slug}/{draw_number}"
        
        try:
            logger.info(f"Fetching {lottery_slug} draw #{draw_number}...")
            
            # Use session to handle cookies
            session = requests.Session()
            
            # First request - may get cookie-setting page
            response = session.get(url, headers=self.headers, timeout=15)
            
            # Check for cookie protection
            if 'setCookie' in response.text and 'location.reload' in response.text:
                logger.debug(f"Cookie protection detected for {lottery_slug} #{draw_number}")
                
                # Extract cookie value from JavaScript
                import time
                cookie_match = re.search(r"setCookie\('([^']+)','([^']+)',", response.text)
                if cookie_match:
                    cookie_name = cookie_match.group(1)
                    cookie_value = cookie_match.group(2)
                    
                    # Set the cookie manually
                    session.cookies.set(cookie_name, cookie_value, domain='.nlb.lk', path='/')
                
                # Wait and make second request
                time.sleep(3)
                response = session.get(url, headers=self.headers, timeout=15)
            
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            if self.debug:
                os.makedirs(f'nlb/{lottery_slug}', exist_ok=True)
                debug_file = f"nlb/{lottery_slug}/nlb_{lottery_slug}_{draw_number}_scrape.html"
                self._save_debug_html(soup, debug_file)
            
            # Parse the result page
            # Structure: <div class="lresult"> contains the lottery result
            lresult = soup.find('div', class_='lresult')
            if not lresult:
                logger.warning(f"No result div found for {lottery_slug} #{draw_number}")
                return None
            
            # Extract draw number from <p><b>Draw No.:</b> 177</p>
            draw_elem = lresult.find('p', string=re.compile(r'Draw No\.:', re.I))
            if not draw_elem:
                draw_elem = lresult.find('h1')
            
            extracted_draw = str(draw_number)  # Default to provided number
            if draw_elem:
                draw_text = draw_elem.get_text()
                draw_match = re.search(r'\d+', draw_text)
                if draw_match:
                    extracted_draw = draw_match.group(0)
            
            # Extract date from <p><b>Date:</b> Thursday January 01, 2026</p>
            date_elem = lresult.find('p', string=re.compile(r'Date:', re.I))
            draw_date = datetime.now()
            if date_elem:
                date_text = date_elem.get_text()
                # Remove "Date:" prefix and parse
                date_str = re.sub(r'Date:', '', date_text, flags=re.I).strip()
                draw_date = self._parse_date(date_str)
            
            # Extract winning numbers with ball type categorization
            # Supports: Letter, Zodiac, Super Number, Regular Number, Promotional
            winning_numbers = []
            ball_lists = lresult.find_all('ol', class_='B')
            for ball_list in ball_lists:
                balls = ball_list.find_all('li', class_=re.compile(r'Number-|Zodiac|Color|Letter', re.I))
                for ball in balls:
                    # Skip "More" buttons
                    if 'More' in ball.get('class', []):
                        continue
                    
                    ball_text = ball.get_text(strip=True)
                    if not ball_text:
                        continue
                    
                    ball_classes = ball.get('class', [])
                    ball_title = ball.get('title', '')
                    
                    # Determine ball type based on CSS classes and title
                    ball_type = 'number'  # default
                    
                    if 'Letter' in ball_classes or ball_title == 'Letter':
                        ball_type = 'letter'
                    elif 'Zodiac' in ball_classes or ball_title == 'Zodiac':
                        ball_type = 'zodiac'
                    elif ball_title == 'Super Number' or ('Circle' in ball_classes and 'Red' in ball_classes):
                        ball_type = 'super'
                    elif 'Number-1' in ' '.join(ball_classes) and 'Square' in ball_classes:
                        # Promotional draw numbers (Square Blue)
                        ball_type = 'promotional'
                    elif re.match(r'^\d{1,2}$', ball_text):
                        # Regular number
                        ball_type = 'number'
                    
                    # Store as structured data: {"type": "letter", "value": "U"}
                    winning_numbers.append({
                        "type": ball_type,
                        "value": ball_text
                    })
            
            # Extract prize amount if available (from prize structure section)
            prize_amount = None
            prize_text = soup.find('div', class_='superprize')
            if prize_text:
                prize_match = re.search(r'Rs\.\s*([\d,]+\.?\d*)', prize_text.get_text())
                if prize_match:
                    prize_amount = prize_match.group(1).replace(',', '')
            
            result = {
                'lottery_name': lottery_slug.replace('-', '_'),
                'draw_number': extracted_draw,
                'draw_date': draw_date,
                'winning_numbers': winning_numbers,
                'prize_amount': prize_amount,
                'additional_data': {
                    'source_url': url,
                    'scrape_method': 'individual_draw'
                }
            }
            
            logger.info(f"NLB: Extracted {lottery_slug} draw #{extracted_draw} - {len(winning_numbers)} numbers")
            
            return result
            
        except Exception as e:
            logger.error(f"Error scraping {lottery_slug} #{draw_number}: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
            return None
    
    def scrape_latest_results(self) -> List[Dict]:
        """Scrape NLB results using flexible patterns (NOT hardcoded selectors)"""
        try:
            logger.info(f"Fetching NLB results from: {self.results_url}")
            response = requests.get(self.results_url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            if self.debug:
                os.makedirs('nlb/misc', exist_ok=True)
                self._save_debug_html(soup, 'nlb/misc/nlb_debug.html')
            
            results = []
            
            # Strategy 1: Look for tables using regex patterns
            tables = soup.find_all('table', class_=re.compile(r'result|lottery|draw', re.I))
            if not tables:
                tables = soup.find_all('table')
            
            for table in tables:
                parsed = self._parse_table_results(table)
                results.extend(parsed)
            
            # Strategy 2: Look for divs/cards using regex
            if not results:
                sections = soup.find_all('div', class_=re.compile(r'result|lottery|card', re.I))
                for section in sections:
                    data = self._parse_result_section(section)
                    if data:
                        results.append(data)
            
            # Strategy 3: Text pattern matching for all NLB lotteries
            if not results:
                print("No structured NLB results found. Trying text patterns...")
                results = self._parse_from_text(soup)
            
            logger.info(f"NLB: Found {len(results)} lottery results")
            return results
        except Exception as e:
            logger.error(f"Error scraping NLB: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
            return []
    
    def _parse_table_results(self, table) -> List[Dict]:
        """Parse table using pattern matching for all NLB lotteries"""
        results = []
        try:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) < 2:
                    continue
                
                row_text = ' '.join([cell.get_text(strip=True) for cell in cells])
                
                # Pattern for all NLB lottery types
                lottery_match = re.search(
                    r'(MAHAJANA SAMPATHA|VASANA SAMPATHA|GOVISETHA|SUPIRI WASANA|DHANA NIDHANAYA|SATURDAY SUPER BALL|SUNDAY MEGA JACKPOT|SHANIDA PATTARE|KOTIPATHI PATTARE)',
                    row_text, re.I
                )
                
                if lottery_match:
                    lottery_name = lottery_match.group(1)
                    draw_match = re.search(r'Draw\s*[#:]?\s*(\d+)', row_text, re.I)
                    draw_number = draw_match.group(1) if draw_match else None
                    date_match = re.search(r'\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4}', row_text)
                    draw_date = self._parse_date(date_match.group(0)) if date_match else datetime.now()
                    numbers = re.findall(r'\b(\d{1,2})\b', row_text)
                    winning_numbers = [n for n in numbers if int(n) < 100][:10]
                    
                    results.append({
                        'lottery_name': lottery_name.lower().replace(' ', '_'),
                        'draw_number': draw_number,
                        'draw_date': draw_date,
                        'winning_numbers': winning_numbers,
                        'prize_amount': None
                    })
        except:
            pass
        return results
    
    def _parse_result_section(self, section) -> Optional[Dict]:
        """Parse section using flexible patterns for all NLB lotteries"""
        try:
            text = section.get_text(separator=' ', strip=True)
            
            lottery_names = [
                'MAHAJANA SAMPATHA', 'VASANA SAMPATHA', 'GOVISETHA', 
                'SUPIRI WASANA', 'DHANA NIDHANAYA', 'SATURDAY SUPER BALL',
                'SUNDAY MEGA JACKPOT', 'SHANIDA PATTARE', 'KOTIPATHI PATTARE'
            ]
            
            lottery_found = None
            for name in lottery_names:
                if name.upper() in text.upper():
                    lottery_found = name
                    break
            
            if lottery_found:
                draw_match = re.search(r'Draw\s*[#:]?\s*(\d+)|#(\d+)', text, re.I)
                draw_number = draw_match.group(1) or draw_match.group(2) if draw_match else None
                date_match = re.search(r'\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4}', text)
                draw_date = self._parse_date(date_match.group(0)) if date_match else datetime.now()
                numbers = re.findall(r'\b(\d{1,2})\b', text)
                winning_numbers = [n for n in numbers if int(n) < 100][:10]
                
                return {
                    'lottery_name': lottery_found.lower().replace(' ', '_'),
                    'draw_number': draw_number,
                    'draw_date': draw_date,
                    'winning_numbers': winning_numbers,
                    'prize_amount': None
                }
        except:
            pass
        return None
    
    def _parse_from_text(self, soup) -> List[Dict]:
        """Parse text for all NLB lottery types"""
        results = []
        text = soup.get_text()
        
        if self.debug:
            print("\n=== NLB TEXT PARSING ===")
        
        # Pattern for all NLB lotteries
        pattern = r'(MAHAJANA SAMPATHA|MAHAJANA\s*SAMPATHA|VASANA SAMPATHA|VASANA\s*SAMPATHA|GOVISETHA|SUPIRI WASANA|SUPIRI\s*WASANA|DHANA NIDHANAYA|DHANA\s*NIDHANAYA|SATURDAY SUPER BALL|SUNDAY MEGA JACKPOT|SHANIDA PATTARE|KOTIPATHI PATTARE)'
        matches = re.findall(pattern, text, re.IGNORECASE)
        
        if self.debug:
            print(f"Found {len(matches)} NLB lottery mentions")
        
        for lottery_name in set(matches):
            lottery_clean = lottery_name.strip()
            lottery_pos = text.find(lottery_name)
            if lottery_pos > -1:
                context = text[lottery_pos:lottery_pos + 300]
                draw_match = re.search(r'Draw\s*[#:]?\s*(\d+)|#(\d+)', context, re.I)
                draw_number = draw_match.group(1) or draw_match.group(2) if draw_match else None
                date_match = re.search(r'\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4}', context)
                number_matches = re.findall(r'\b(\d{1,2})\b', context)
                winning_nums = [n for n in number_matches if int(n) < 100][:10]
                
                results.append({
                    'lottery_name': lottery_clean.lower().replace(' ', '_'),
                    'draw_number': draw_number,
                    'draw_date': self._parse_date(date_match.group(0)) if date_match else datetime.now(),
                    'winning_numbers': winning_nums,
                    'prize_amount': None
                })
        
        return results
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse date string"""
        try:
            date_str = date_str.strip().upper()
            date_str = re.sub(r'(MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY)', '', date_str).strip()
            formats = ['%Y-%b-%d', '%Y-%m-%d', '%d-%b-%Y', '%d/%m/%Y', '%Y/%m/%d', '%d-%m-%Y', '%m/%d/%Y']
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except:
                    continue
            return datetime.now()
        except:
            return datetime.now()
    
    def _save_debug_html(self, soup, filename):
        """Save HTML for debugging"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            print(f"Debug HTML saved to {filename}")
        except:
            pass
    
    def save_results(self, results: List[Dict]) -> int:
        """Save results to database"""
        db = SessionLocal()
        saved_count = 0
        duplicate_count = 0
        
        try:
            for result in results:
                existing = db.query(LotteryResult).filter(
                    LotteryResult.lottery_name == result['lottery_name'],
                    LotteryResult.draw_number == result['draw_number']
                ).first()
                
                if not existing:
                    lottery_result = LotteryResult(
                        lottery_name=result['lottery_name'],
                        draw_number=result['draw_number'],
                        draw_date=result['draw_date'],
                        winning_numbers=result['winning_numbers'],
                        prize_amount=result.get('prize_amount'),
                        additional_data=result.get('additional_data', {})
                    )
                    db.add(lottery_result)
                    saved_count += 1
                    logger.info(f"NLB: Saved {result['lottery_name']} draw #{result['draw_number']}")
                else:
                    duplicate_count += 1
                    logger.debug(f"NLB: Duplicate skipped - {result['lottery_name']} draw #{result['draw_number']}")
            
            db.commit()
            if duplicate_count > 0:
                logger.info(f"NLB: Skipped {duplicate_count} duplicates")
            return saved_count
        except Exception as e:
            logger.error(f"Error saving NLB results: {e}")
            db.rollback()
            return 0
        finally:
            db.close()


def run_scraper(debug=False):
    """Run both scrapers"""
    logger.info("="*60)
    logger.info("Starting lottery scraper")
    logger.info("="*60)
    
    logger.info("--- DLB (Development Lotteries Board) ---")
    dlb = DLBScraper(debug=debug)
    dlb_results = dlb.scrape_latest_results()
    dlb_saved = dlb.save_results(dlb_results)
    logger.info(f"DLB: Found {len(dlb_results)} results, saved {dlb_saved} new")
    
    if debug and dlb_results:
        for r in dlb_results[:3]:
            logger.debug(f"  - {r['lottery_name']}: #{r['draw_number']}, Numbers: {r['winning_numbers']}")
    
    logger.info("--- NLB (National Lotteries Board) ---")
    nlb = NLBScraper(debug=debug)
    nlb_results = nlb.scrape_latest_results()
    nlb_saved = nlb.save_results(nlb_results)
    logger.info(f"NLB: Found {len(nlb_results)} results, saved {nlb_saved} new")
    
    if debug and nlb_results:
        for r in nlb_results[:3]:
            logger.debug(f"  - {r['lottery_name']}: #{r['draw_number']}, Numbers: {r['winning_numbers']}")
    
    logger.info("="*60)
    logger.info(f"Scraper completed. Total saved: {dlb_saved + nlb_saved}")
    logger.info("="*60)
    return dlb_saved + nlb_saved


if __name__ == "__main__":
    import sys
    debug_mode = '--debug' in sys.argv
    print("Sri Lankan Lottery Scraper\n" + "=" * 60)
    if debug_mode:
        print("🔍 DEBUG MODE - HTML will be saved for inspection")
    run_scraper(debug=debug_mode)
