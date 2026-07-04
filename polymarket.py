import requests

BASE_URL = "https://data-api.polymarket.com"


def get_user_positions(wallet_address):
    """
    Downloads every open position for one wallet.
    """

    url = f"{BASE_URL}/positions?user={wallet_address}"

    try:
        response = requests.get(url, timeout=20)

        if response.status_code != 200:
            return []

        return response.json()

    except Exception as e:
        print(e)
        return []


def normalize_positions(raw):

    positions = []

    for item in raw:

        market = item.get("title") or item.get("question") or ""
        if not market:
            continue

        size = 0
        try:
            size = float(item.get("size", 0))
        except:
            size = 0

        positions.append({
            "market": market,
            "side": "YES",  # default fallback (Polymarket positions are directional but not cleanly labeled here)
            "size": size,
            "wallet": item.get("proxyWallet")
        })

    return positions

def load_wallet(wallet):
    """
    Convenience wrapper.
    """

    raw = get_user_positions(wallet)

    return normalize_positions(raw, wallet)
