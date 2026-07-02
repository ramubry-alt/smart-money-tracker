import requests

BASE_URL = "https://gamma-api.polymarket.com"


def get_user_positions(wallet_address):
    """
    Fetch current positions from Polymarket API.
    """
    try:
        url = f"{BASE_URL}/positions?user={wallet_address}"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception:
        return []


def normalize_positions(raw_positions):
    """
    Normalize Polymarket API response into:
    { market, side, size }
    """

    normalized = []

    for p in raw_positions:
        try:
            market = (
                p.get("condition", {}).get("title")
                or p.get("market", {}).get("question")
                or "Unknown Market"
            )

            size = float(p.get("size", 0) or 0)

            side = p.get("side") or p.get("position") or "YES"

            normalized.append({
                "market": market,
                "side": side.upper(),
                "size": size
            })

        except Exception:
            continue

    return normalized
