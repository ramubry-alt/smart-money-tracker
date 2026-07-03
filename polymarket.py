import requests
import json

BASE_URL = "https://gamma-api.polymarket.com"


def get_user_positions(wallet_address):
    """
    Try multiple possible Polymarket endpoints to find REAL wallet positions.
    """

    endpoints = [
        f"{BASE_URL}/positions?user={wallet_address}",
        f"{BASE_URL}/portfolio?user={wallet_address}",
        f"{BASE_URL}/user-positions?user={wallet_address}",
        f"{BASE_URL}/events?user={wallet_address}",
    ]

    for url in endpoints:
        try:
            res = requests.get(url, timeout=10)
            if res.status_code != 200:
                continue

            data = res.json()

            if data and isinstance(data, list) and len(data) > 0:
                print("\n================ WORKING ENDPOINT ================")
                print(url)
                print("=================================================\n")

                return data

        except:
            continue

    print("No valid endpoint found.")
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
