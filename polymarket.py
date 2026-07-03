import requests
from collections import defaultdict

# -----------------------------------------
# CONFIG
# -----------------------------------------
INDEXER_URL = "https://clob.polymarket.com"


# -----------------------------------------
# FETCH WALLET TRADE HISTORY (INDEXED DATA)
# -----------------------------------------
def get_user_positions(wallet_address):
    """
    Pull indexed trade/fill data for a wallet.

    This is the closest public approximation to true Polymarket positions.
    """

    # Try multiple realistic endpoints (indexer implementations vary)
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
                print(f"\n✅ Using indexer endpoint: {url}")
                print(f"Wallet {wallet_address} → {len(data)} records")

                return data

        except Exception:
            continue

    print(f"\n⚠️ No indexed data found for wallet: {wallet_address}")
    return []


# -----------------------------------------
# NORMALIZE INTO POSITIONS
# -----------------------------------------
def normalize_positions(raw_trades):
    """
    Convert trade history → aggregated positions.

    We reconstruct exposure by summing:
    (market + outcome side)
    """

    positions = defaultdict(float)

    for trade in raw_trades:
        try:
            # -----------------------------
            # MARKET IDENTIFICATION
            # -----------------------------
            market = (
                trade.get("market")
                or trade.get("title")
                or trade.get("question")
                or trade.get("event")
                or "UNKNOWN MARKET"
            )

            if not market:
                continue

            # -----------------------------
            # OUTCOME / SIDE
            # -----------------------------
            side = (
                trade.get("side")
                or trade.get("outcome")
                or trade.get("token")
                or "YES"
            )

            side = str(side).upper()

            # -----------------------------
            # SIZE / NOTIONAL VALUE
            # -----------------------------
            size = (
                trade.get("size")
                or trade.get("amount")
                or trade.get("quantity")
                or trade.get("filled_size")
                or 0
            )

            try:
                size = float(size)
            except:
                size = 0.0

            # ignore zero-size noise
            if size <= 0:
                continue

            key = (market, side)
            positions[key] += size

        except Exception:
            continue

    # -----------------------------------------
    # FLATTEN OUTPUT
    # -----------------------------------------
    result = []

    for (market, side), size in positions.items():
        result.append({
            "market": market,
            "side": side,
            "size": round(size, 4)
        })

    return result
