import requests
import json

BASE_URL = "http://localhost:5001"

def test_v21_features():
    print("--- Testing v2.1 Features ---")
    
    # 1. Test New Emoji Themes (Space)
    print("\n1. Testing 'Space' Emoji Theme...")
    try:
        r = requests.post(f"{BASE_URL}/api/new-puzzle", json={
            "variation_type": "emoji",
            "theme": "space"
        })
        data = r.json()
        print(f"Success: {data['success']}")
        print(f"Symbols Used: {' '.join(data['symbols'][:3])}...")
    except:
        print("Server not running, skipping live test.")

    # 2. Test Daily Challenge
    print("\n2. Testing Daily Challenge...")
    try:
        r = requests.post(f"{BASE_URL}/api/new-puzzle", json={
            "daily_challenge": True
        })
        data = r.json()
        print(f"Is Daily: {data.get('is_daily')}")
    except:
        pass

    # 3. Test Multiplayer Versus
    print("\n3. Testing Multiplayer Versus (Match ID: 1234)...")
    try:
        r1 = requests.post(f"{BASE_URL}/api/multiplayer/versus", json={"match_id": "1234"})
        r2 = requests.post(f"{BASE_URL}/api/multiplayer/versus", json={"match_id": "1234"})
        p1 = r1.json()['puzzle']
        p2 = r2.json()['puzzle']
        print(f"Puzzles Match: {p1 == p2}")
    except:
        pass

if __name__ == "__main__":
    test_v21_features()
