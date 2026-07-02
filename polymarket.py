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
        market = item.get("title") or item.get("question") or ""
        if any(x in market for x in ["2020", "2021", "2022"]):
    continue
    try:
            market = (
                item.get("title")
                or item.get("question")
                or item.get("market", {}).get("question")
                or "Unknown Market"
            )

            # 🔥 REALISTIC SIZE EXTRACTION (Polymarket structure varies)
            size = 0

            if isinstance(item.get("outcomePositions"), list):
                for op in item["outcomePositions"]:
                    size += float(op.get("size", 0) or 0)

            elif item.get("size") is not None:
                size = float(item.get("size") or 0)

            elif item.get("amount") is not None:
                size = float(item.get("amount") or 0)

            # side detection
            side = (
                item.get("side")
                or item.get("outcome")
                or "YES"
            )

            positions.append({
                "market": market,
                "side": str(side).upper(),
                "size": round(size, 2)
            })

        except Exception:
            continue

    return positions
