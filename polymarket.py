import requests

BASE_URL = "https://gamma-api.polymarket.com"


def get_user_positions(wallet_address):
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
            market = item.get("title") or item.get("question") or ""

            # FILTER OUT OLD / NOISE MARKETS
            if any(x in market for x in ["2020", "2021", "2022"]):
                continue

            size = 0

            if isinstance(item.get("outcomePositions"), list):
                for op in item["outcomePositions"]:
                    size += float(op.get("size", 0) or 0)

            side = item.get("side") or item.get("outcome") or "YES"

            positions.append({
                "market": market,
                "side": str(side).upper(),
                "size": round(size, 2)
            })

        except Exception:
            continue

    return positions
