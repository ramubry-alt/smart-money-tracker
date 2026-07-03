import requests

BASE_URL = "https://gamma-api.polymarket.com"


def get_user_positions(wallet_address):
    """
    Pull raw positions from Polymarket API.
    Also prints ONE sample record for debugging (first wallet only).
    """
    try:
        url = f"{BASE_URL}/events?user={wallet_address}"
        res = requests.get(url, timeout=10)
        res.raise_for_status()

        data = res.json()

        # Print sample only once per run (first wallet call)
        if data:
            print("\n========== SAMPLE API RECORD ==========")
            print(data[0])
            print("=======================================\n")

        return data

    except Exception as e:
        print(f"API error for wallet {wallet_address}: {e}")
        return []


def normalize_positions(raw_positions):
    """
    Normalize Polymarket data into a consistent format.
    We DO NOT assume field names — we extract safely.
    """

    positions = []

    for item in raw_positions:
        try:
            market = (
                item.get("title")
                or item.get("question")
                or item.get("name")
                or "Unknown Market"
            )

            market_lower = market.lower()

            # Filter out obviously stale markets
            if any(x in market_lower for x in ["2020", "2021", "2022"]):
                continue

            # Extract side safely
            side = item.get("side") or item.get("outcome") or "YES"
            side = str(side).upper()

            # Extract size safely (multiple possible API shapes)
            size = 0.0

            if isinstance(item.get("outcomePositions"), list):
                for op in item["outcomePositions"]:
                    try:
                        size += float(op.get("size", 0) or 0)
                    except:
                        pass

            # fallback if API uses different field
            if size == 0:
                size = float(item.get("size", 0) or 0)

            positions.append({
                "market": market,
                "side": side,
                "size": round(size, 2)
            })

        except Exception:
            continue

    return positions
