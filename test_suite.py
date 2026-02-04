"""
Comprehensive Testing Suite for Sudoku Variations
Tests all variations, API endpoints, and error handling
"""

import requests
import json
import time
from typing import Dict, List
import sys

# Configuration
API_BASE_URL = "http://localhost:5001"
TIMEOUT = 10

# Test counters
tests_run = 0
tests_passed = 0
tests_failed = 0


def print_header(text: str):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_test(name: str, passed: bool, message: str = ""):
    """Print test result"""
    global tests_run, tests_passed, tests_failed
    tests_run += 1
    
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} | {name}")
    
    if message:
        print(f"       {message}")
    
    if passed:
        tests_passed += 1
    else:
        tests_failed += 1


def test_health_check():
    """Test health check endpoint"""
    print_header("Health Check")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=TIMEOUT)
        passed = response.status_code == 200
        data = response.json() if passed else {}
        
        print_test(
            "Health endpoint responds",
            passed,
            f"Status: {data.get('status', 'N/A')}, Version: {data.get('version', 'N/A')}"
        )
        
        return passed
    except Exception as e:
        print_test("Health endpoint responds", False, str(e))
        return False


def test_variations_available():
    """Test variations listing endpoint"""
    print_header("Variations Available")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/variations/available", timeout=TIMEOUT)
        passed = response.status_code == 200
        data = response.json() if passed else {}
        
        print_test("Variations endpoint responds", passed)
        
        if passed and data.get('success'):
            variations = data.get('variations', {})
            print_test(
                "Variations data structure",
                len(variations) > 0,
                f"Found {len(variations)} variation types"
            )
            
            # Test each variation has required fields
            for var_type, var_info in variations.items():
                has_fields = all(
                    key in var_info
                    for key in ['description', 'target_audience', 'difficulty_modifier']
                )
                print_test(
                    f"Variation '{var_type}' has metadata",
                    has_fields,
                    f"Themes: {len(var_info.get('themes', []))}"
                )
        
        return passed
    except Exception as e:
        print_test("Variations endpoint responds", False, str(e))
        return False


def test_classic_puzzle():
    """Test classic puzzle generation"""
    print_header("Classic Puzzle Generation")
    
    difficulties = ['easy', 'medium', 'hard']
    
    for difficulty in difficulties:
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/new-puzzle",
                json={
                    'difficulty': difficulty,
                    'variation_type': 'classic',
                    'language': 'en'
                },
                timeout=TIMEOUT
            )
            
            passed = response.status_code == 200
            data = response.json() if passed else {}
            
            if passed and data.get('success'):
                puzzle = data.get('puzzle', [])
                has_zeros = any(0 in row for row in puzzle)
                valid_size = len(puzzle) == 9 and all(len(row) == 9 for row in puzzle)
                
                print_test(
                    f"Classic {difficulty} puzzle",
                    passed and has_zeros and valid_size,
                    f"Grid size: 9x9, Has empty cells: {has_zeros}"
                )
            else:
                print_test(f"Classic {difficulty} puzzle", False, data.get('error', 'Unknown error'))
                
        except Exception as e:
            print_test(f"Classic {difficulty} puzzle", False, str(e))


def test_emoji_variations():
    """Test emoji puzzle generation"""
    print_header("Emoji Puzzle Variations")
    
    themes = ['animals', 'fruits', 'faces']
    
    for theme in themes:
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/new-puzzle",
                json={
                    'difficulty': 'medium',
                    'variation_type': 'emoji',
                    'theme': theme,
                    'language': 'en'
                },
                timeout=TIMEOUT
            )
            
            passed = response.status_code == 200
            data = response.json() if passed else {}
            
            if passed and data.get('success'):
                symbols = data.get('symbols', [])
                print_test(
                    f"Emoji {theme} theme",
                    len(symbols) == 9,
                    f"Symbols: {' '.join(symbols[:3])}..."
                )
            else:
                print_test(f"Emoji {theme} theme", False, data.get('error', 'Unknown error'))
                
        except Exception as e:
            print_test(f"Emoji {theme} theme", False, str(e))


def test_color_variations():
    """Test color puzzle generation"""
    print_header("Color Puzzle Variations")
    
    themes = ['rainbow', 'pastel']
    
    for theme in themes:
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/new-puzzle",
                json={
                    'difficulty': 'easy',
                    'variation_type': 'color',
                    'theme': theme,
                    'language': 'en'
                },
                timeout=TIMEOUT
            )
            
            passed = response.status_code == 200
            data = response.json() if passed else {}
            
            if passed and data.get('success'):
                symbols = data.get('symbols', [])
                print_test(
                    f"Color {theme} theme",
                    len(symbols) == 9,
                    f"Colors: {symbols[0]}, {symbols[1]}..."
                )
            else:
                print_test(f"Color {theme} theme", False, data.get('error', 'Unknown error'))
                
        except Exception as e:
            print_test(f"Color {theme} theme", False, str(e))


def test_symbol_variations():
    """Test symbol puzzle generation"""
    print_header("Symbol Puzzle Variations")
    
    themes = ['shapes', 'greek']
    
    for theme in themes:
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/new-puzzle",
                json={
                    'difficulty': 'hard',
                    'variation_type': 'symbol',
                    'theme': theme,
                    'language': 'en'
                },
                timeout=TIMEOUT
            )
            
            passed = response.status_code == 200
            data = response.json() if passed else {}
            
            if passed and data.get('success'):
                symbols = data.get('symbols', [])
                print_test(
                    f"Symbol {theme} theme",
                    len(symbols) == 9,
                    f"Symbols: {' '.join(symbols[:3])}..."
                )
            else:
                print_test(f"Symbol {theme} theme", False, data.get('error', 'Unknown error'))
                
        except Exception as e:
            print_test(f"Symbol {theme} theme", False, str(e))


def test_error_handling():
    """Test error handling"""
    print_header("Error Handling")
    
    # Test invalid difficulty
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/new-puzzle",
            json={
                'difficulty': 'invalid',
                'variation_type': 'classic'
            },
            timeout=TIMEOUT
        )
        
        print_test(
            "Reject invalid difficulty",
            response.status_code == 400,
            f"Status code: {response.status_code}"
        )
    except Exception as e:
        print_test("Reject invalid difficulty", False, str(e))
    
    # Test missing data
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/validate-solution",
            json={},
            timeout=TIMEOUT
        )
        
        print_test(
            "Reject missing solution data",
            response.status_code == 400,
            f"Status code: {response.status_code}"
        )
    except Exception as e:
        print_test("Reject missing solution data", False, str(e))
    
    # Test invalid cell position for hint
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/get-hint",
            json={'row': 10, 'col': 10},
            timeout=TIMEOUT
        )
        
        print_test(
            "Reject invalid hint position",
            response.status_code == 400,
            f"Status code: {response.status_code}"
        )
    except Exception as e:
        print_test("Reject invalid hint position", False, str(e))


def test_full_game_flow():
    """Test complete game flow"""
    print_header("Full Game Flow Test")
    
    try:
        # 1. Generate puzzle
        response = requests.post(
            f"{API_BASE_URL}/api/new-puzzle",
            json={
                'difficulty': 'easy',
                'variation_type': 'emoji',
                'theme': 'animals'
            },
            timeout=TIMEOUT
        )
        
        puzzle_data = response.json()
        print_test("1. Generate puzzle", puzzle_data.get('success', False))
        
        if not puzzle_data.get('success'):
            return
        
        # 2. Get hint
        time.sleep(0.5)
        response = requests.post(
            f"{API_BASE_URL}/api/get-hint",
            json={'row': 0, 'col': 2},
            timeout=TIMEOUT
        )
        
        hint_data = response.json()
        print_test("2. Get hint", hint_data.get('success', False))
        
        # 3. Validate incomplete solution
        time.sleep(0.5)
        response = requests.post(
            f"{API_BASE_URL}/api/validate-solution",
            json={'solution': puzzle_data.get('puzzle', [])},
            timeout=TIMEOUT
        )
        
        validate_data = response.json()
        print_test(
            "3. Validate incomplete solution",
            validate_data.get('success', False) and not validate_data.get('is_correct', True)
        )
        
        # 4. Submit score
        time.sleep(0.5)
        response = requests.post(
            f"{API_BASE_URL}/api/submit-score",
            json={
                'username': 'TestUser',
                'time': 120,
                'hints': 1
            },
            timeout=TIMEOUT
        )
        
        score_data = response.json()
        print_test("4. Submit score", score_data.get('success', False))
        
        # 5. Get leaderboard
        time.sleep(0.5)
        response = requests.get(
            f"{API_BASE_URL}/api/leaderboard",
            timeout=TIMEOUT
        )
        
        leaderboard_data = response.json()
        print_test("5. Fetch leaderboard", leaderboard_data.get('success', False))
        
        # 6. Get KPI
        time.sleep(0.5)
        response = requests.get(
            f"{API_BASE_URL}/api/kpi",
            timeout=TIMEOUT
        )
        
        kpi_data = response.json()
        print_test("6. Fetch KPI stats", kpi_data.get('success', False))
        
    except Exception as e:
        print_test("Full game flow", False, str(e))


def test_performance():
    """Test performance metrics"""
    print_header("Performance Tests")
    
    # Test puzzle generation speed
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/new-puzzle",
            json={'difficulty': 'medium', 'variation_type': 'classic'},
            timeout=TIMEOUT
        )
        
        elapsed = time.time() - start_time
        print_test(
            "Puzzle generation speed",
            elapsed < 2.0,
            f"Generated in {elapsed:.3f}s (target: < 2.0s)"
        )
    except Exception as e:
        print_test("Puzzle generation speed", False, str(e))
    
    # Test concurrent requests
    import concurrent.futures
    
    def make_request():
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/new-puzzle",
                json={'difficulty': 'easy', 'variation_type': 'classic'},
                timeout=TIMEOUT
            )
            return response.status_code == 200
        except:
            return False
    
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request) for _ in range(10)]
        results = [f.result() for f in futures]
    
    elapsed = time.time() - start_time
    success_rate = sum(results) / len(results) * 100
    
    print_test(
        "Concurrent requests",
        success_rate >= 90,
        f"Success rate: {success_rate:.1f}%, Time: {elapsed:.3f}s for 10 requests"
    )


def print_summary():
    """Print test summary"""
    print("\n" + "=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)
    print(f"  Total Tests: {tests_run}")
    print(f"  ✅ Passed: {tests_passed}")
    print(f"  ❌ Failed: {tests_failed}")
    
    if tests_failed == 0:
        print("\n  🎉 ALL TESTS PASSED! 🎉")
    else:
        print(f"\n  ⚠️  {tests_failed} test(s) failed")
    
    print("=" * 70 + "\n")
    
    return tests_failed == 0


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  SUDOKU VARIATIONS - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print(f"  API Base URL: {API_BASE_URL}")
    print(f"  Timeout: {TIMEOUT}s")
    print("=" * 70)
    
    # Check if server is running
    if not test_health_check():
        print("\n❌ ERROR: Server is not running or not responding!")
        print(f"Please start the server at {API_BASE_URL}")
        sys.exit(1)
    
    # Run all test suites
    test_variations_available()
    test_classic_puzzle()
    test_emoji_variations()
    test_color_variations()
    test_symbol_variations()
    test_error_handling()
    test_full_game_flow()
    test_performance()
    
    # Print summary
    success = print_summary()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
