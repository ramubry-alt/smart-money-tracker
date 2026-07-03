import requests
import json

BASE_URL = "https://gamma-api.polymarket.com"


def get_user_positions(wallet_address):
    """
    HARD DEBUG MODE:
    Print EXACT raw API response so we can see real structure.
    """

    try:
        url = f"{BASE_URL}/events?user={wallet_address}"
        res = requests.get(url, timeout=10)
        res.raise_for_status()

        data = res.json()

        print("\n================ RAW API DEBUG ================\n")
        print(f"Wallet: {wallet_address}")
        print(f"Type: {type(data)}")
        print(f"Length: {len(data) if isinstance(data, list) else 'N/A'}")

        if isinstance(data, list) and len(data) > 0:
            print("\n--- FIRST ITEM ---")
            print(json.dumps(data[0], indent=2)[:3000])

        print("\n===============================================\n")

        return data

    except Exception as e:
        print(f"API ERROR: {e}")
        return []


def normalize_positions(raw_positions):
    """
    TEMPORARY: pass-through (we disable logic until we see real API format)
    """

    positions = []

    for item in raw_positions:
        try:
            market = item.get("title") or item.get("question") or "UNKNOWN"

            positions.append({
                "market": market,
                "side": "YES",
                "size": 0.0
            })

        except:
            continue

    return positions
