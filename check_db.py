"""Check database entries to see current ball structure"""
from database import SessionLocal, LotteryResult
import json

db = SessionLocal()
results = db.query(LotteryResult).limit(5).all()

print('=== SAMPLE DATABASE ENTRIES ===\n')
for r in results:
    print(f'{r.lottery_name} #{r.draw_number}:')
    print(f'  Date: {r.draw_date}')
    print(f'  Numbers: {json.dumps(r.winning_numbers, indent=4)}')
    print()

db.close()
