# API Integration Guide
## How to Use the Lottery API in Other Software

Once deployed to Render.com, your API URL will be:
`https://lottery-scraper-api.onrender.com`

## Authentication

### Option 1: Public API (No Authentication)
If you don't set `API_KEY` environment variable, anyone can use the API.

```python
import requests

# No authentication needed
response = requests.get('https://lottery-scraper-api.onrender.com/api/stats')
print(response.json())
```

### Option 2: API Key Authentication (Recommended)
If you set `API_KEY` in Render, all requests need the API key.

```python
import requests

API_KEY = "your-secret-api-key-here"
headers = {"X-API-Key": API_KEY}

# All requests include the header
response = requests.get(
    'https://lottery-scraper-api.onrender.com/api/stats',
    headers=headers
)
print(response.json())
```

## Example Integrations

### 1. Python - Get Latest Results

```python
import requests

API_URL = "https://lottery-scraper-api.onrender.com"
API_KEY = "your-secret-api-key"  # Optional, if authentication enabled

headers = {"X-API-Key": API_KEY} if API_KEY else {}

def get_latest_results(limit=10, board=None):
    """Get latest lottery results"""
    params = {"limit": limit}
    if board:
        params["board"] = board  # "DLB" or "NLB"
    
    response = requests.get(
        f"{API_URL}/api/results/latest",
        headers=headers,
        params=params
    )
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 403:
        print("Error: Invalid or missing API key")
    else:
        print(f"Error: {response.status_code}")
    
    return None

# Usage
results = get_latest_results(limit=5, board="DLB")
for result in results:
    print(f"{result['lottery_name']} - Draw #{result['draw_number']}")
    print(f"Numbers: {result['winning_numbers']}")
    print(f"Date: {result['draw_date']}")
    print("-" * 50)
```

### 2. Python - Verify Lottery Ticket

```python
def verify_ticket(lottery_name, ticket_numbers, draw_number=None):
    """Check if ticket numbers match winning numbers"""
    
    payload = {
        "lottery_name": lottery_name,
        "ticket_numbers": ticket_numbers,
        "draw_number": draw_number  # Optional
    }
    
    response = requests.post(
        f"{API_URL}/api/verify",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        print(f"Error: {response.status_code}")
        return None

# Usage
ticket = ["U", "08", "14", "21", "25"]
result = verify_ticket("ada_kotipathi", ticket, draw_number="2865")

if result and result['is_winner']:
    print(f"🎉 WINNER! Matched numbers: {result['matched_numbers']}")
    print(f"Prize info: {result.get('prize_info', 'N/A')}")
else:
    print("Not a winner this time")
```

### 3. Python - OCR Ticket Scanner Integration

```python
import cv2
import pytesseract
import requests

API_URL = "https://lottery-scraper-api.onrender.com"
API_KEY = "your-secret-api-key"
headers = {"X-API-Key": API_KEY}

def scan_ticket_ocr(image_path):
    """Extract numbers from ticket using OCR"""
    img = cv2.imread(image_path)
    text = pytesseract.image_to_string(img)
    
    # Parse numbers from OCR text (customize based on ticket format)
    numbers = []
    for line in text.split('\n'):
        # Extract alphanumeric characters
        tokens = line.split()
        for token in tokens:
            if token.isalnum():
                numbers.append(token)
    
    return numbers

def verify_scanned_ticket(image_path, lottery_name):
    """Full workflow: OCR → API verification"""
    
    # Step 1: OCR scan
    print("Scanning ticket...")
    ticket_numbers = scan_ticket_ocr(image_path)
    print(f"Detected numbers: {ticket_numbers}")
    
    # Step 2: Get latest draw for this lottery
    response = requests.get(
        f"{API_URL}/api/results/{lottery_name}",
        headers=headers,
        params={"limit": 1}
    )
    
    if response.status_code != 200:
        return {"error": "Could not fetch lottery results"}
    
    latest_draw = response.json()[0]
    draw_number = latest_draw['draw_number']
    
    # Step 3: Verify ticket
    verify_response = requests.post(
        f"{API_URL}/api/verify",
        headers=headers,
        json={
            "lottery_name": lottery_name,
            "ticket_numbers": ticket_numbers,
            "draw_number": draw_number
        }
    )
    
    return verify_response.json()

# Usage
result = verify_scanned_ticket("ticket.jpg", "ada_kotipathi")
print(result)
```

### 4. JavaScript/Node.js - Get Results

```javascript
const axios = require('axios');

const API_URL = 'https://lottery-scraper-api.onrender.com';
const API_KEY = 'your-secret-api-key';

async function getLatestResults(limit = 10, board = null) {
    try {
        const params = { limit };
        if (board) params.board = board;
        
        const response = await axios.get(`${API_URL}/api/results/latest`, {
            headers: { 'X-API-Key': API_KEY },
            params: params
        });
        
        return response.data;
    } catch (error) {
        if (error.response?.status === 403) {
            console.error('Invalid or missing API key');
        } else {
            console.error('Error:', error.message);
        }
        return null;
    }
}

// Usage
getLatestResults(5, 'DLB').then(results => {
    results.forEach(result => {
        console.log(`${result.lottery_name} - Draw #${result.draw_number}`);
        console.log(`Numbers: ${JSON.stringify(result.winning_numbers)}`);
    });
});
```

### 5. JavaScript - Verify Ticket

```javascript
async function verifyTicket(lotteryName, ticketNumbers, drawNumber = null) {
    try {
        const response = await axios.post(
            `${API_URL}/api/verify`,
            {
                lottery_name: lotteryName,
                ticket_numbers: ticketNumbers,
                draw_number: drawNumber
            },
            {
                headers: { 'X-API-Key': API_KEY }
            }
        );
        
        return response.data;
    } catch (error) {
        console.error('Verification error:', error.message);
        return null;
    }
}

// Usage
verifyTicket('ada_kotipathi', ['U', '08', '14', '21', '25'], '2865')
    .then(result => {
        if (result?.is_winner) {
            console.log('🎉 WINNER!');
            console.log('Matched:', result.matched_numbers);
        } else {
            console.log('Not a winner');
        }
    });
```

### 6. Mobile App (React Native / Flutter)

#### React Native Example

```javascript
import axios from 'axios';

const API_URL = 'https://lottery-scraper-api.onrender.com';
const API_KEY = 'your-secret-api-key';

export const lotteryAPI = {
    getLatestResults: async (limit = 10, board = null) => {
        const params = { limit };
        if (board) params.board = board;
        
        const response = await axios.get(`${API_URL}/api/results/latest`, {
            headers: { 'X-API-Key': API_KEY },
            params
        });
        
        return response.data;
    },
    
    verifyTicket: async (lotteryName, ticketNumbers, drawNumber = null) => {
        const response = await axios.post(
            `${API_URL}/api/verify`,
            {
                lottery_name: lotteryName,
                ticket_numbers: ticketNumbers,
                draw_number: drawNumber
            },
            {
                headers: { 'X-API-Key': API_KEY }
            }
        );
        
        return response.data;
    }
};

// Usage in component
import { lotteryAPI } from './api';

function LotteryResults() {
    const [results, setResults] = useState([]);
    
    useEffect(() => {
        lotteryAPI.getLatestResults(10, 'DLB')
            .then(data => setResults(data))
            .catch(err => console.error(err));
    }, []);
    
    return (
        <View>
            {results.map(result => (
                <Text key={result.id}>
                    {result.lottery_name} - {result.winning_numbers.join(', ')}
                </Text>
            ))}
        </View>
    );
}
```

## API Endpoints Reference

### GET /api/lotteries
Get all available lottery types
```bash
curl -H "X-API-Key: your-key" \
  https://lottery-scraper-api.onrender.com/api/lotteries
```

### GET /api/results/latest
Get latest results across all lotteries
```bash
curl -H "X-API-Key: your-key" \
  "https://lottery-scraper-api.onrender.com/api/results/latest?limit=10&board=DLB"
```

### GET /api/results/{lottery_name}
Get results for specific lottery
```bash
curl -H "X-API-Key: your-key" \
  "https://lottery-scraper-api.onrender.com/api/results/ada_kotipathi?limit=5"
```

### GET /api/results/date/{date}
Get results by date (format: YYYY-MM-DD)
```bash
curl -H "X-API-Key: your-key" \
  https://lottery-scraper-api.onrender.com/api/results/date/2026-01-05
```

### POST /api/verify
Verify ticket numbers
```bash
curl -X POST -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"lottery_name":"ada_kotipathi","ticket_numbers":["U","08","14"],"draw_number":"2865"}' \
  https://lottery-scraper-api.onrender.com/api/verify
```

### GET /api/stats
Get database statistics
```bash
curl -H "X-API-Key: your-key" \
  https://lottery-scraper-api.onrender.com/api/stats
```

### POST /api/scrape
Manually trigger scraper
```bash
curl -X POST -H "X-API-Key: your-key" \
  https://lottery-scraper-api.onrender.com/api/scrape
```

## Error Handling

### Status Codes
- `200` - Success
- `400` - Bad request (invalid parameters)
- `403` - Forbidden (invalid/missing API key)
- `404` - Not found
- `500` - Server error

### Example Error Response
```json
{
    "detail": "Invalid or missing API Key. Add 'X-API-Key' header with your API key."
}
```

## Rate Limiting

Render free tier has no strict rate limits, but:
- Be respectful with requests
- Cache results when possible
- Don't spam the scraper endpoint
- Consider adding your own rate limiting in production

## Security Best Practices

1. **Keep API Key Secret**
   - Never commit API keys to Git
   - Use environment variables
   - Rotate keys periodically

2. **Use HTTPS Only**
   - Render provides automatic HTTPS
   - Never send API keys over HTTP

3. **Validate Input**
   - Sanitize user input before API calls
   - Validate ticket numbers format
   - Handle errors gracefully

4. **Monitor Usage**
   - Check Render logs for suspicious activity
   - Set up alerts for errors
   - Track API usage patterns

## Example: Complete Lottery Shop Software

```python
# lottery_shop.py
import requests
from datetime import datetime

class LotteryAPI:
    def __init__(self, api_url, api_key=None):
        self.api_url = api_url
        self.headers = {"X-API-Key": api_key} if api_key else {}
    
    def get_latest_results(self, board=None, limit=10):
        params = {"limit": limit}
        if board:
            params["board"] = board
        
        response = requests.get(
            f"{self.api_url}/api/results/latest",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    def verify_ticket(self, lottery_name, ticket_numbers, draw_number=None):
        payload = {
            "lottery_name": lottery_name,
            "ticket_numbers": ticket_numbers
        }
        if draw_number:
            payload["draw_number"] = draw_number
        
        response = requests.post(
            f"{self.api_url}/api/verify",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()

# Usage
api = LotteryAPI(
    "https://lottery-scraper-api.onrender.com",
    "your-secret-api-key"
)

# Display today's results
print("Today's Lottery Results")
print("=" * 50)

results = api.get_latest_results(limit=5)
for result in results:
    print(f"\n{result['lottery_name'].upper()}")
    print(f"Draw: #{result['draw_number']}")
    print(f"Date: {result['draw_date']}")
    
    # Handle both old and new format
    numbers = result['winning_numbers']
    if numbers and isinstance(numbers[0], dict):
        # New format with ball types
        display = [n['value'] for n in numbers]
    else:
        # Old format (plain strings)
        display = numbers
    
    print(f"Winning Numbers: {' - '.join(map(str, display))}")
    print("-" * 50)

# Verify a customer's ticket
print("\n\nTicket Verification")
print("=" * 50)

ticket = ["U", "08", "14", "21", "25"]
verification = api.verify_ticket("ada_kotipathi", ticket, "2865")

if verification['is_winner']:
    print("🎉 CONGRATULATIONS! This is a WINNING ticket!")
    print(f"Matched numbers: {', '.join(verification['matched_numbers'])}")
    if verification.get('prize_info'):
        print(f"Prize: {verification['prize_info']}")
else:
    print("Sorry, this ticket is not a winner.")
```

## Need Help?

- API Documentation: `https://lottery-scraper-api.onrender.com/docs`
- Test endpoints interactively in the docs
- Check logs in Render dashboard for errors
