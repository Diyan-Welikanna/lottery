"""Show examples of each ball type in the database"""
from database import SessionLocal, LotteryResult
import json

db = SessionLocal()

print('=== BALL TYPE EXAMPLES ===\n')

# Example of LETTER (DLB)
print('1. LETTER (DLB - Ada Kotipathi):')
result = db.query(LotteryResult).filter(LotteryResult.lottery_name == 'ada_kotipathi').first()
if result:
    print(f'   {result.lottery_name} #{result.draw_number}')
    print(f'   Numbers: {json.dumps(result.winning_numbers, indent=4)}')
print()

# Example of LETTER (NLB - Mega Power)
print('2. LETTER + SUPER (NLB - Mega Power):')
result = db.query(LotteryResult).filter(LotteryResult.lottery_name == 'mega_power').first()
if result:
    print(f'   {result.lottery_name} #{result.draw_number}')
    print(f'   Numbers: {json.dumps(result.winning_numbers, indent=4)}')
print()

# Example of ZODIAC (NLB - Suba Dawasak)
print('3. ZODIAC + PROMOTIONAL (NLB - Suba Dawasak):')
result = db.query(LotteryResult).filter(LotteryResult.lottery_name == 'suba_dawasak').first()
if result:
    print(f'   {result.lottery_name} #{result.draw_number}')
    print(f'   Numbers: {json.dumps(result.winning_numbers, indent=4)}')
print()

# Example of ZODIAC (NLB - Handahana)
print('4. ZODIAC (NLB - Handahana):')
result = db.query(LotteryResult).filter(LotteryResult.lottery_name == 'handahana').first()
if result:
    print(f'   {result.lottery_name} #{result.draw_number}')
    print(f'   Numbers: {json.dumps(result.winning_numbers, indent=4)}')
print()

# Count by ball type
print('\n=== BALL TYPE STATISTICS ===')
all_results = db.query(LotteryResult).all()
ball_types = {'letter': 0, 'zodiac': 0, 'super': 0, 'number': 0, 'promotional': 0}
for r in all_results:
    for ball in r.winning_numbers:
        if isinstance(ball, dict) and 'type' in ball:
            ball_types[ball['type']] = ball_types.get(ball['type'], 0) + 1

for ball_type, count in ball_types.items():
    print(f'  {ball_type.upper()}: {count} balls')

print(f'\nTotal results in database: {len(all_results)}')

db.close()
