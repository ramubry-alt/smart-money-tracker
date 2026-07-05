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


def normalize_positions(raw, wallet=None):

    print("\n========== FIRST POSITION ==========\n")

    if raw:
        from pprint import pprint
        pprint(raw[0])

    print("\n====================================\n")

    positions = []

    for item in raw:
        print("\nFIELDS:")
        print(item.keys())
        break
        
        market = item.get("title") or item.get("question") or ""
        if not market:
            continue

        # --------------------------
        # REAL SIDE DETECTION
        # --------------------------
        side = "YES"

        if isinstance(item.get("outcomePositions"), list):

            # pick largest outcome position as direction proxy
            best_size = 0

            for op in item["outcomePositions"]:
                try:
                    size = float(op.get("size", 0))
                except:
                    size = 0

                if size > best_size:
                    best_size = size
                    side = op.get("outcome") or "YES"

        try:
            size = float(item.get("size", 0))
        except:
            size = 0

        positions.append({
            "market": market,
            "side": str(side).upper(),
            "size": size,
            "wallet": wallet or item.get("proxyWallet")
        })

    return positions
    
def load_wallet(wallet):
    """
    Convenience wrapper.
    """

    raw = get_user_positions(wallet)

    return normalize_positions(raw, wallet)
