import requests
from collections import defaultdict

CLOB_URL = "https://clob.polymarket.com"


# ----------------------------
# FETCH TRADES (CLOBBED DATA)
# ----------------------------
def get_user_positions(wallet_address):
    """
    Pull user fills/trades from CLOB API.
    This is the ONLY reliable way to reconstruct exposure.
    """

    url = f"{CLOB_URL}/trades?user={wallet_address}"

    try:
        res = requests.get(url, timeout=15)

        if res.status_code != 200:
            print(f"❌ CLOB error {res.status_code} for {wallet_address}")
            return []

        data = res.json()

        print(f"\n✅ Trades fetched for {wallet_address}: {len(data)} records")

        return data

    except Exception as e:
        print(f"❌ CLOB request failed: {e}")
        return []


# ----------------------------
# NORMALIZE INTO POSITIONS
# ----------------------------
def normalize_positions(raw_trades):
    """
    Convert trades → pseudo-positions.
    We aggregate buys per market + side.
    """

    positions = defaultdict(float)

    for trade in raw_trades:
        try:
            market = (
                trade.get("market")
                or trade.get("title")
                or trade.get("question")
                or "UNKNOWN"
            )

            # side: YES / NO (or LONG / SHORT)
            side = (
                trade.get("side")
                or trade.get("outcome")
                or "YES"
            )

            side = str(side).upper()

            # size / notional
            size = (
                trade.get("size")
                or trade.get("amount")
                or trade.get("quantity")
                or 0
            )

            try:
                size = float(size)
            except:
                size = 0.0

            key = (market, side)
            positions[key] += size

        except:
            continue

    # convert back to structured list
    result = []

    for (market, side), size in positions.items():
        result.append({
            "market": market,
            "side": side,
            "size": round(size, 4)
        })

    return result
