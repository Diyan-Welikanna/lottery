"""
Ball Type Categorization - Comprehensive Validation
Tests all ball type detection across NLB and DLB lotteries
"""
from database import SessionLocal, LotteryResult
import json

def test_ball_types():
    """Validate ball type categorization across all lotteries"""
    db = SessionLocal()
    
    print("=" * 70)
    print("BALL TYPE CATEGORIZATION - VALIDATION REPORT")
    print("=" * 70)
    
    # Test cases
    test_cases = [
        {
            'name': 'Mega Power - Letter + Super + Numbers',
            'lottery': 'mega_power',
            'expected_types': ['letter', 'super', 'number']
        },
        {
            'name': 'Suba Dawasak - Zodiac + Numbers + Promotional',
            'lottery': 'suba_dawasak',
            'expected_types': ['zodiac', 'number', 'promotional']
        },
        {
            'name': 'Handahana - Zodiac + Numbers',
            'lottery': 'handahana',
            'expected_types': ['zodiac', 'number']
        },
        {
            'name': 'Ada Kotipathi (DLB) - Letter + Numbers',
            'lottery': 'ada_kotipathi',
            'expected_types': ['letter', 'number']
        },
        {
            'name': 'Govisetha - Letter + Numbers',
            'lottery': 'govisetha',
            'expected_types': ['letter', 'number']
        }
    ]
    
    print("\n1. INDIVIDUAL LOTTERY TESTS")
    print("-" * 70)
    
    passed = 0
    failed = 0
    
    for test in test_cases:
        result = db.query(LotteryResult).filter(
            LotteryResult.lottery_name == test['lottery']
        ).first()
        
        if not result:
            print(f"\n❌ FAILED: {test['name']}")
            print(f"   Reason: No results found in database")
            failed += 1
            continue
        
        # Extract ball types from result
        ball_types = set()
        for ball in result.winning_numbers:
            if isinstance(ball, dict) and 'type' in ball:
                ball_types.add(ball['type'])
        
        # Check if expected types are present
        expected = set(test['expected_types'])
        if expected.issubset(ball_types):
            print(f"\n✅ PASSED: {test['name']}")
            print(f"   Lottery: {result.lottery_name} #{result.draw_number}")
            print(f"   Expected types: {', '.join(expected)}")
            print(f"   Found types: {', '.join(ball_types)}")
            print(f"   Sample: {json.dumps(result.winning_numbers[:3], indent=11)}")
            passed += 1
        else:
            print(f"\n❌ FAILED: {test['name']}")
            print(f"   Expected: {', '.join(expected)}")
            print(f"   Found: {', '.join(ball_types)}")
            print(f"   Missing: {', '.join(expected - ball_types)}")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"TEST SUMMARY: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70)
    
    # Global statistics
    print("\n2. GLOBAL BALL TYPE STATISTICS")
    print("-" * 70)
    
    all_results = db.query(LotteryResult).all()
    ball_counts = {}
    lottery_ball_types = {}
    
    for result in all_results:
        lottery_name = result.lottery_name
        if lottery_name not in lottery_ball_types:
            lottery_ball_types[lottery_name] = set()
        
        for ball in result.winning_numbers:
            if isinstance(ball, dict) and 'type' in ball:
                ball_type = ball['type']
                ball_counts[ball_type] = ball_counts.get(ball_type, 0) + 1
                lottery_ball_types[lottery_name].add(ball_type)
    
    print(f"\nTotal Lotteries: {len(lottery_ball_types)}")
    print(f"Total Results: {len(all_results)}")
    print(f"\nBall Type Distribution:")
    for ball_type, count in sorted(ball_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {ball_type.upper():<15} : {count:>3} balls")
    
    print("\n3. LOTTERY BALL TYPE PATTERNS")
    print("-" * 70)
    
    for lottery, types in sorted(lottery_ball_types.items()):
        types_str = ", ".join(sorted(types))
        print(f"  {lottery:<25} : {types_str}")
    
    # Verify specific requirements
    print("\n4. USER REQUIREMENT VERIFICATION")
    print("-" * 70)
    
    # Count NLB letter lotteries
    nlb_letter_lotteries = [
        name for name, types in lottery_ball_types.items()
        if 'letter' in types and name not in ['ada_kotipathi', 'shanida', 'lagna_wasana', 
                                                'supiri_dhana_sampatha', 'super_ball', 'kapruka',
                                                'jayoda', 'sasiri', 'jaya_sampatha']
    ]
    
    # Count zodiac lotteries
    zodiac_lotteries = [
        name for name, types in lottery_ball_types.items()
        if 'zodiac' in types
    ]
    
    # Check Mega Power super numbers
    mega_power_has_super = 'mega_power' in lottery_ball_types and 'super' in lottery_ball_types['mega_power']
    
    # Count DLB letter lotteries
    dlb_letter_lotteries = [
        name for name, types in lottery_ball_types.items()
        if 'letter' in types and name in ['ada_kotipathi', 'shanida', 'lagna_wasana', 
                                           'supiri_dhana_sampatha', 'super_ball', 'kapruka',
                                           'jayoda', 'sasiri', 'jaya_sampatha']
    ]
    
    print(f"\n✅ NLB Lotteries with LETTERS: {len(nlb_letter_lotteries)}")
    for lottery in nlb_letter_lotteries:
        print(f"   - {lottery}")
    
    print(f"\n✅ NLB Lotteries with ZODIAC SIGNS: {len(zodiac_lotteries)}")
    for lottery in zodiac_lotteries:
        print(f"   - {lottery}")
    
    print(f"\n{'✅' if mega_power_has_super else '❌'} Mega Power has SUPER NUMBERS: {mega_power_has_super}")
    if mega_power_has_super:
        mega_result = db.query(LotteryResult).filter(
            LotteryResult.lottery_name == 'mega_power'
        ).first()
        super_balls = [b for b in mega_result.winning_numbers if b.get('type') == 'super']
        print(f"   Example super numbers: {', '.join([b['value'] for b in super_balls])}")
    
    print(f"\n✅ DLB Lotteries with LETTERS: {len(dlb_letter_lotteries)}")
    for lottery in dlb_letter_lotteries:
        print(f"   - {lottery}")
    
    print("\n" + "=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)
    
    db.close()
    
    return passed == len(test_cases)

if __name__ == "__main__":
    success = test_ball_types()
    exit(0 if success else 1)
