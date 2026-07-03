import requests
from collections import defaultdict

# -------------------------------------------------
# CONFIG (INDEXER LAYER)
# -------------------------------------------------
INDEXER_URL = "https://clob.polymarket.com"


# -------------------------------------------------
# FETCH WALLET FILL HISTORY (INDEXER STYLE)
# -------------------------------------------------
def get_user_positions(wallet_address):
    """
    Pull indexed fills/trades for a wallet.

    This is the ONLY realistic way to reconstruct positions
    without private API keys.
    """

    endpoints = [
        f"{INDEXER_URL}/fills?user={wallet_address}",
        f"{INDEXER_URL}/trades?user={wallet_address}",
        f"{INDEXER_URL}/history?user={wallet_address}",
    ]

    for url in endpoints:
        try:
            res = requests.get(url, timeout=15)

            if res.status_code != 200:
                continue

            data = res.json()

            if isinstance(data, list) and len(data) > 0:
                print(f"✅ INDEXER HIT: {wallet_address} → {len(data)} records")
                return data

        except Exception:
            continue

    print(f"⚠️ No indexer data for wallet: {wallet_address}")
    return []


# -------------------------------------------------
# NORMALIZE INTO POSITION EXPOSURE
# -------------------------------------------------
def normalize_positions(raw_trades):
    """
    Converts raw fills → aggregated market exposure
    """

    positions = defaultdict(float)

    for t in raw_trades:
        try:
            # -------------------------
            # MARKET NAME
            # -------------------------
            market = (
                t.get("market")
                or t.get("title")
                or t.get("question")
                or t.get("event_title")
                or "UNKNOWN"
            )

            if not market:
                continue

            # -------------------------
            # SIDE (YES / NO)
            # -------------------------
            side = (
                t.get("side")
                or t.get("outcome")
                or t.get("token")
                or "YES"
            )

            side = str(side).upper()

            # -------------------------
            # SIZE (NOTIONAL / FILL)
            # -------------------------
            size = (
                t.get("size")
                or t.get("amount")
                or t.get("filled_size")
                or t.get("quantity")
                or 0
            )

            try:
                size = float(size)
            except:
                size = 0.0

            if size <= 0:
                continue

            key = (market, side)
            positions[key] += size

        except:
            continue

    # -------------------------
    # FLATTEN OUTPUT
    # -------------------------
    result = []

    for (market, side), size in positions.items():
        result.append({
            "market": market,
            "side": side,
            "size": round(size, 4)
        })

    return result
