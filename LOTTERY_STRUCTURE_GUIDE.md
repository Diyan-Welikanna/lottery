# Sri Lankan Lottery Results - Complete Structure Guide

## Table of Contents
1. [DLB Lottery Structure](#dlb-development-lotteries-board)
2. [NLB Lottery Structure](#nlb-national-lotteries-board)
3. [Ball Type System](#ball-type-system)
4. [Database Schema](#database-schema)
5. [API Response Format](#api-response-format)

---

## DLB (Development Lotteries Board)

### Overview
- **Website**: https://www.dlb.lk/result/en
- **Total Lotteries**: 9
- **Result Update Time**: Daily around 10 PM - 6 AM
- **Structure**: Tab-based interface with all lotteries on one page

### DLB Lottery List

#### 1. **Ada Kotipathi** (ඇඩ කෝටිපති)
- **Board**: DLB
- **Slug**: `ada_kotipathi`
- **Structure**: Letter + 4 Numbers
- **Example Result**:
  ```json
  {
    "lottery_name": "ada_kotipathi",
    "draw_number": "2864",
    "draw_date": "2026-01-04",
    "winning_numbers": [
      {"type": "letter", "value": "Y"},
      {"type": "number", "value": "08"},
      {"type": "number", "value": "21"},
      {"type": "number", "value": "71"},
      {"type": "number", "value": "76"}
    ]
  }
  ```

#### 2. **Shanida** (ශනිදා)
- **Board**: DLB
- **Slug**: `shanida`
- **Structure**: Letter + 4 Numbers
- **Example**: `G, 10, 21, 65, 70`

#### 3. **Lagna Wasana** (ලග්න වාසනා)
- **Board**: DLB
- **Slug**: `lagna_wasana`
- **Structure**: 4 Numbers (Note: Name suggests zodiac, may vary)
- **Example**: `28, 42, 51, 54`

#### 4. **Supiri Dhana Sampatha** (සුපිරි ධන සම්පත)
- **Board**: DLB
- **Slug**: `supiri_dhana_sampatha`
- **Structure**: Letter + 6 Numbers
- **Example**: `S, 0, 4, 8, 5, 8, 1`

#### 5. **Super Ball**
- **Board**: DLB
- **Slug**: `super_ball`
- **Structure**: Letter + 4 Numbers
- **Example**: `I, 17, 18, 44, 47`

#### 6. **Kapruka** (කප්රුක)
- **Board**: DLB
- **Slug**: `kapruka`
- **Structure**: Letter + 5 Numbers
- **Example**: `X, 19, 36, 55, 57, 10`

#### 7. **Jayoda** (ජයෝද)
- **Board**: DLB
- **Slug**: `jayoda`
- **Structure**: Letter + 4 Numbers
- **Example**: `V, 15, 30, 54, 55`

#### 8. **Sasiri** (සසිරි)
- **Board**: DLB
- **Slug**: `sasiri`
- **Structure**: 3 Numbers (No letter detected in current samples)
- **Example**: `18, 35, 36`

#### 9. **Jaya Sampatha** (ජය සම්පත)
- **Board**: DLB
- **Slug**: `jaya_sampatha`
- **Structure**: Letter + 4 Numbers
- **Example**: `S, 8, 5, 8, 1`

### DLB HTML Structure

```html
<!-- DLB Results Page Structure -->
<div class="tab-content">
  <div id="lottery0" class="tab-pane">
    <div class="lot_main_result">
      
      <!-- Lottery Name -->
      <h2 class="lot_m_re_heading">Ada Kotipathi</h2>
      
      <!-- Draw Info -->
      <h3 class="lot_m_re_date">Draw Number - 2864 | 2026-Jan-04 Sunday</h3>
      
      <!-- Winning Numbers -->
      <ul class="result_detail_result">
        <li><h6 class="eng_letter">Y</h6></li>
        <li><h6 class="number_shanida number_circle">08</h6></li>
        <li><h6 class="number_shanida number_circle">21</h6></li>
        <li><h6 class="number_shanida number_circle">71</h6></li>
        <li><h6 class="number_shanida number_circle">76</h6></li>
      </ul>
      
    </div>
  </div>
</div>
```

### DLB Ball Type Detection
- **Letter**: `<h6 class="eng_letter">` or `<h6 class="lagna_letter">`
- **Number**: `<h6 class="number_shanida number_circle">`
- **Zodiac**: TBD (may appear in Lagna Wasana)

---

## NLB (National Lotteries Board)

### Overview
- **Website**: https://www.nlb.lk/results/
- **Total Lotteries**: 8
- **Result Update Time**: Varies by lottery
- **Structure**: Individual pages per lottery, cookie protection enabled

### NLB Lottery List

#### 1. **Suba Dawasak** (සුභ දවසක්)
- **Board**: NLB
- **Slug**: `suba-dawasak`
- **URL Pattern**: `https://www.nlb.lk/results/suba-dawasak/{draw_number}`
- **Starting Draw Number**: 177 (Jan 1, 2026)
- **Structure**: **Zodiac** + 3 Numbers + **Promotional Draw** (4 numbers)
- **Example Result**:
  ```json
  {
    "lottery_name": "suba_dawasak",
    "draw_number": "177",
    "draw_date": "2026-01-01",
    "winning_numbers": [
      {"type": "zodiac", "value": "VIRGO"},
      {"type": "number", "value": "27"},
      {"type": "number", "value": "39"},
      {"type": "number", "value": "46"},
      {"type": "promotional", "value": "1"},
      {"type": "promotional", "value": "2"},
      {"type": "promotional", "value": "0"},
      {"type": "promotional", "value": "1"}
    ]
  }
  ```

#### 2. **NLB Jaya**
- **Board**: NLB
- **Slug**: `nlb-jaya`
- **URL Pattern**: `https://www.nlb.lk/results/nlb-jaya/{draw_number}`
- **Starting Draw Number**: 329 (Jan 1, 2026)
- **Structure**: Letter + 4 Numbers
- **Example**: `A, 3, 5, 1, 2`

#### 3. **Ada Sampatha** (ඇඩ සම්පත)
- **Board**: NLB
- **Slug**: `ada-sampatha`
- **URL Pattern**: `https://www.nlb.lk/results/ada-sampatha/{draw_number}`
- **Starting Draw Number**: 636 (Jan 1, 2026)
- **Structure**: 9 Numbers + Letter (Letter at end!)
- **Example**: `0, 0, 5, 0, 0, 4, 5, 0, 0, H`

#### 4. **Handahana** (හඳහන)
- **Board**: NLB
- **Slug**: `handahana`
- **URL Pattern**: `https://www.nlb.lk/results/handahana/{draw_number}`
- **Starting Draw Number**: 1370 (Jan 1, 2026)
- **Structure**: **Zodiac** + 4 Numbers
- **Example Result**:
  ```json
  {
    "winning_numbers": [
      {"type": "zodiac", "value": "CANCER"},
      {"type": "number", "value": "13"},
      {"type": "number", "value": "15"},
      {"type": "number", "value": "34"},
      {"type": "number", "value": "50"}
    ]
  }
  ```

#### 5. **Dhana Nidhanaya** (ධන නිධානය)
- **Board**: NLB
- **Slug**: `dhana-nidhanaya`
- **URL Pattern**: `https://www.nlb.lk/results/dhana-nidhanaya/{draw_number}`
- **Starting Draw Number**: 2091 (Jan 1, 2026)
- **Structure**: Letter + 4 Numbers
- **Example**: `Z, 48, 71, 72, 78`

#### 6. **Mega Power** ⭐ (Special!)
- **Board**: NLB
- **Slug**: `mega-power`
- **URL Pattern**: `https://www.nlb.lk/results/mega-power/{draw_number}`
- **Starting Draw Number**: 2409 (Jan 1, 2026)
- **Structure**: Letter + **SUPER NUMBER** + 4 Numbers
- **Special Feature**: Super Number (RED Circle) - higher prize tier
- **Example Result**:
  ```json
  {
    "lottery_name": "mega_power",
    "draw_number": "2409",
    "winning_numbers": [
      {"type": "letter", "value": "U"},
      {"type": "super", "value": "21"},  // ⭐ SUPER NUMBER!
      {"type": "number", "value": "18"},
      {"type": "number", "value": "23"},
      {"type": "number", "value": "31"},
      {"type": "number", "value": "76"}
    ]
  }
  ```

#### 7. **Govisetha** (ගෝවිසෙත)
- **Board**: NLB
- **Slug**: `govisetha`
- **URL Pattern**: `https://www.nlb.lk/results/govisetha/{draw_number}`
- **Starting Draw Number**: 4303 (Jan 1, 2026)
- **Structure**: Letter + 4 Numbers
- **Example**: `R, 22, 33, 39, 62`

#### 8. **Mahajana Sampatha** (මහජන සම්පත)
- **Board**: NLB
- **Slug**: `mahajana-sampatha`
- **URL Pattern**: `https://www.nlb.lk/results/mahajana-sampatha/{draw_number}`
- **Starting Draw Number**: 6061 (Jan 1, 2026)
- **Structure**: Letter + 6 Numbers
- **Example**: `H, 4, 7, 4, 5, 0, 0`

### NLB HTML Structure

```html
<!-- NLB Results Page Structure (with Cookie Protection) -->
<div class="lresult">
  
  <!-- Draw Info -->
  <p><b>Draw No.:</b> 2409</p>
  <p><b>Date:</b> Thursday January 02, 2026</p>
  
  <!-- Winning Numbers -->
  <ol class="B">
    <!-- Letter Ball -->
    <li class="Letter Circle Blue bU" title="Letter">U</li>
    
    <!-- Super Number (Mega Power only - RED!) -->
    <li class="Number-2 Circle Red b21" title="Super Number">21</li>
    
    <!-- Regular Numbers (Yellow) -->
    <li class="Number-2 Circle Yellow b18" title="Number-1">18</li>
    <li class="Number-2 Circle Yellow b23" title="Number-2">23</li>
    <li class="Number-2 Circle Yellow b31" title="Number-3">31</li>
    <li class="Number-2 Circle Yellow b76" title="Number-4">76</li>
  </ol>
  
  <!-- Zodiac Ball (Suba Dawasak/Handahana) -->
  <ol class="B">
    <li class="Zodiac Square Blue bD" title="Zodiac">CANCER</li>
    <!-- Numbers... -->
  </ol>
  
  <!-- Promotional Draw (Suba Dawasak only) -->
  <span>Promotional Draw</span>
  <ol class="B">
    <li class="Number-1 Square Blue b0" title="Number-1">0</li>
    <li class="Number-1 Square Blue b8" title="Number-2">8</li>
    <li class="Number-1 Square Blue b0" title="Number-3">0</li>
    <li class="Number-1 Square Blue b5" title="Number-4">5</li>
  </ol>
  
</div>
```

### NLB Cookie Protection
NLB websites use JavaScript cookie protection:
```javascript
// Server sends cookie-setting page first
setCookie('__test','1234567890abcdef', 1);
location.reload();

// Scraper must:
// 1. Detect cookie protection page
// 2. Extract cookie value from JavaScript
// 3. Set cookie in session
// 4. Wait 3 seconds
// 5. Request again with cookie
```

---

## Ball Type System

### Ball Types (5 Total)

#### 1. **LETTER** (A-Z)
- **Used In**: 13 lotteries (6 NLB + 7 DLB)
- **CSS Classes**: 
  - NLB: `Letter Circle Blue`
  - DLB: `eng_letter` or `lagna_letter`
- **Display**: Blue circle
- **Examples**: A, B, C, ..., Z

#### 2. **ZODIAC** (12 Signs)
- **Used In**: 2 NLB lotteries (Suba Dawasak, Handahana)
- **CSS Class**: `Zodiac Square Blue`
- **Display**: Purple square
- **Values**: ARIES, TAURUS, GEMINI, CANCER, LEO, VIRGO, LIBRA, SCORPIO, SAGITTARIUS, CAPRICORN, AQUARIUS, PISCES

#### 3. **SUPER NUMBER** ⭐
- **Used In**: 1 lottery (Mega Power only)
- **CSS Class**: `Number-2 Circle Red` (RED is key!)
- **Display**: Red pulsing circle
- **Range**: 0-99
- **Special**: Worth higher prize tier

#### 4. **REGULAR NUMBER**
- **Used In**: All lotteries
- **CSS Classes**:
  - NLB: `Number-2 Circle Yellow`
  - DLB: `number_shanida number_circle`
- **Display**: Purple gradient circle
- **Range**: 0-99

#### 5. **PROMOTIONAL** (Bonus)
- **Used In**: 1 lottery (Suba Dawasak only)
- **CSS Class**: `Number-1 Square Blue`
- **Display**: Green square
- **Count**: 4 numbers
- **Purpose**: Bonus draw for additional prizes

### Ball Type Detection Logic

```python
# NLB Detection
ball_classes = ball.get('class', [])
ball_title = ball.get('title', '')

if 'Letter' in ball_classes or ball_title == 'Letter':
    ball_type = 'letter'
elif 'Zodiac' in ball_classes or ball_title == 'Zodiac':
    ball_type = 'zodiac'
elif ball_title == 'Super Number' or ('Circle' in ball_classes and 'Red' in ball_classes):
    ball_type = 'super'  # RED Circle = Super Number!
elif 'Number-1' in ' '.join(ball_classes) and 'Square' in ball_classes:
    ball_type = 'promotional'
else:
    ball_type = 'number'

# DLB Detection
h6_classes = h6.get('class', [])

if 'eng_letter' in h6_classes or 'lagna_letter' in h6_classes:
    ball_type = 'letter'
elif re.match(r'^[A-Z]$', num_text):
    ball_type = 'letter'  # Single uppercase letter
elif len(num_text) > 2:
    ball_type = 'zodiac'  # Long text like "CANCER"
else:
    ball_type = 'number'
```

---

## Database Schema

### LotteryResult Table

```python
class LotteryResult(Base):
    __tablename__ = "lottery_results"
    
    id = Column(Integer, primary_key=True, index=True)
    lottery_name = Column(String, index=True)           # e.g., "mega_power"
    draw_number = Column(String, index=True)            # e.g., "2409"
    draw_date = Column(DateTime, index=True)            # e.g., "2026-01-05"
    winning_numbers = Column(JSON)                      # Array of {type, value}
    prize_amount = Column(String, nullable=True)        # e.g., "Rs. 10,000,000"
    additional_data = Column(JSON, nullable=True)       # Extra metadata
    scraped_at = Column(DateTime, default=datetime.utcnow)  # When scraped
```

### Winning Numbers Format

**New Format (with ball types)**:
```json
[
  {"type": "letter", "value": "U"},
  {"type": "super", "value": "21"},
  {"type": "number", "value": "18"},
  {"type": "number", "value": "23"},
  {"type": "number", "value": "31"},
  {"type": "number", "value": "76"}
]
```

**Legacy Format (plain strings)** - Still supported:
```json
["U", "21", "18", "23", "31", "76"]
```

### Additional Data Format

```json
{
  "source_url": "https://www.nlb.lk/results/mega-power/2409",
  "scrape_method": "individual_draw",
  "cookie_protected": true
}
```

---

## API Response Format

### GET /api/results/latest

```json
[
  {
    "lottery_name": "mega_power",
    "draw_number": "2409",
    "draw_date": "2026-01-05T00:00:00",
    "winning_numbers": [
      {"type": "letter", "value": "U"},
      {"type": "super", "value": "21"},
      {"type": "number", "value": "18"},
      {"type": "number", "value": "23"},
      {"type": "number", "value": "31"},
      {"type": "number", "value": "76"}
    ],
    "prize_amount": null,
    "additional_data": {
      "source_url": "https://www.nlb.lk/results/mega-power/2409",
      "scrape_method": "individual_draw"
    },
    "scraped_at": "2026-01-05T12:37:21.715481"
  }
]
```

### GET /api/lotteries

```json
[
  {
    "name": "mega_power",
    "display_name": "Mega Power",
    "board": "NLB",
    "has_letters": true,
    "has_zodiac": false,
    "has_super": true,
    "url_pattern": "https://www.nlb.lk/results/mega-power/{draw_number}"
  },
  {
    "name": "suba_dawasak",
    "display_name": "Suba Dawasak",
    "board": "NLB",
    "has_letters": false,
    "has_zodiac": true,
    "has_super": false,
    "has_promotional": true
  }
]
```

---

## Summary Statistics

### Lottery Distribution
- **Total Lotteries**: 17
  - NLB: 8
  - DLB: 9

### Ball Type Distribution
- **Lotteries with Letters**: 13
- **Lotteries with Zodiac**: 2 (Suba Dawasak, Handahana)
- **Lotteries with Super Numbers**: 1 (Mega Power)
- **Lotteries with Promotional**: 1 (Suba Dawasak)

### Structure Patterns
1. **Letter + Numbers**: 11 lotteries
2. **Zodiac + Numbers**: 2 lotteries
3. **Letter + Super + Numbers**: 1 lottery (Mega Power)
4. **Numbers Only**: 2 lotteries (Lagna Wasana, Sasiri)
5. **Zodiac + Numbers + Promotional**: 1 lottery (Suba Dawasak)

---

## Notes for Developers

### Important Considerations

1. **Cookie Protection**: NLB requires cookie handling (see NLB section)
2. **Draw Number Gaps**: Not all draw numbers exist (holidays, errors)
3. **Date Parsing**: Multiple date formats used across boards
4. **Ball Order Matters**: First ball is often letter/zodiac
5. **Super Number**: Only Mega Power has this - RED circle class
6. **Promotional Draw**: Only Suba Dawasak has bonus numbers
7. **Letter Position**: Usually first, but Ada Sampatha has it last!
8. **Backward Compatibility**: API supports both old and new formats

### Scraping Best Practices

1. **DLB**: Single page scrape, all lotteries at once
2. **NLB**: Individual draw scraping with cookie session
3. **Rate Limiting**: Wait 3-4 seconds between NLB requests
4. **Error Handling**: Some draws may not exist
5. **Duplicate Prevention**: Check draw_number before saving
6. **Logging**: Comprehensive logging for debugging

### Ticket Verification Requirements

To verify a lottery ticket, you need:
1. **Lottery Name**: Match exact lottery
2. **Draw Number**: Match specific draw
3. **Ball Types**: Verify correct ball types (letter/zodiac/super/number)
4. **Ball Values**: Match exact values in correct order
5. **Prize Tier**: Super numbers = higher tier

---

**Last Updated**: January 5, 2026
**Database Version**: v2.0 (with ball types)
**Total Results Scraped**: 45
