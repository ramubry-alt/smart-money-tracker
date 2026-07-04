from collections import defaultdict
from polymarket import load_wallet


# ---------------------------------------------------------
# CORE ENGINE
# ---------------------------------------------------------

def get_top_consensus(wallets_5, wallets_25):
    """
    Returns:
        five_results, top25_results
    """

    five_positions = []
    top25_positions = []

    # -----------------------------
    # Load wallet positions
    # -----------------------------
    for w in wallets_5:
        five_positions.extend(load_wallet(w))

    for w in wallets_25:
        top25_positions.extend(load_wallet(w))

    # -----------------------------
    # Compute consensus groups
    # -----------------------------
    five = compute_consensus(five_positions, len(wallets_5))
    top25 = compute_consensus(top25_positions, len(wallets_25))

    return five, top25


# ---------------------------------------------------------
# CONSENSUS CORE
# ---------------------------------------------------------

def compute_consensus(positions, wallet_count):
    from collections import defaultdict

    markets = defaultdict(lambda: {"YES": set(), "NO": set(), "size": 0, "wallets": set()})

    for p in positions:

        market = (p.get("market") or "").strip()
        if not market:
            continue

        side = (p.get("side") or "YES").upper()
        wallet = p.get("wallet")

        try:
            size = float(p.get("size", 0))
        except Exception:
            size = 0.0

        if side not in ["YES", "NO"]:
            continue

        markets[market][side].add(wallet)
        markets[market]["wallets"].add(wallet)
        markets[market]["size"] += size

    results = []

    for market, data in markets.items():

        yes_count = len(data["YES"])
        no_count = len(data["NO"])
        total_wallets = len(data["wallets"])

        if total_wallets == 0:
            continue

        if yes_count >= no_count:
            direction = "YES"
            agreement = yes_count
        else:
            direction = "NO"
            agreement = no_count

        # IMPORTANT FIX: normalize by ACTUAL participation, not full wallet set
        agreement_pct = (agreement / total_wallets) * 100

        results.append({
            "market": market,
            "direction": direction,
            "strength": round(agreement_pct, 1),
            "volume": round(data["size"], 2),
        })

    results.sort(key=lambda x: (x["strength"], x["volume"]), reverse=True)

    return results[:10]
