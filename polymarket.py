import requests

BASE_URL = "https://gamma-api.polymarket.com"


def get_user_positions(wallet_address):
    """
    Try ONLY the correct Polymarket indexer-style endpoint pattern.
    This avoids fake 'events' data.
    """

    url = f"{BASE_URL}/positions?user={wallet_address}"

    try:
        res = requests.get(url, timeout=10)

        # If endpoint doesn't exist, fail fast (important)
        if res.status_code != 200:
            print(f"❌ Bad response for {wallet_address}: {res.status_code}")
            return []

        data = res.json()

        print(f"\n✅ Positions fetched for wallet: {wallet_address}")
        print(f"Count: {len(data) if isinstance(data, list) else 'N/A'}")

        return data

    except Exception as e:
        print(f"API error for {wallet_address}: {e}")
        return []


def normalize_positions(raw_positions):
    """
    Extract REAL position structure as defensively as possible.
    """

    positions = []

    for item in raw_positions:
        try:
            market = (
                item.get("title")
                or item.get("question")
                or item.get("market")
                or "UNKNOWN MARKET"
            )

            # Skip empty markets
            if not market or market == "UNKNOWN MARKET":
                continue

            # Extract side safely
            side = (
                item.get("outcome")
                or item.get("side")
                or "YES"
            )

            side = str(side).upper()

            # Extract size safely
            size = 0.0

            if "size" in item:
                try:
                    size = float(item.get("size", 0))
                except:
                    size = 0.0

            positions.append({
                "market": market,
                "side": side,
                "size": round(size, 2)
            })

        except:
            continue

    return positions
