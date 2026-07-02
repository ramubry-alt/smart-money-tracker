import requests

BASE_URL = "https://gamma-api.polymarket.com"


def get_user_positions(wallet_address):
    """
    Get ALL activities and derive positions from them.
    (More reliable than /positions endpoint)
    """
    try:
        url = f"{BASE_URL}/events?user={wallet_address}"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception:
        return []

def normalize_positions(raw):
    positions = []

    for item in raw:
        try:
            market = item.get("title") or item.get("question") or "Unknown Market"

            # 🔥 FIX: extract size from nested fields safely
            size = (
                item.get("size")
                or item.get("amount")
                or item.get("positionSize")
                or item.get("value")
                or 0
            )

            # ensure numeric
            try:
                size = float(size)
            except:
                size = 0

            side = item.get("side") or item.get("outcome") or "YES"

            positions.append({
                "market": market,
                "side": side.upper(),
                "size": size
            })

        except Exception:
            continue

    return positions
