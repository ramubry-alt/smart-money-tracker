from collections import defaultdict
import re
from polymarket import get_user_positions, normalize_positions


# ---------------------------
# MARKET NORMALIZATION
# ---------------------------
def normalize_market_name(market):
    market = market.lower().strip()
    market = re.sub(r"[^a-z0-9\s]", "", market)
    market = re.sub(r"\s+", " ", market)
    return market


# ---------------------------
# WALLET SNAPSHOT
# ---------------------------
def build_wallet_snapshot(wallets):
    all_positions = []

    for wallet in wallets:
        raw = get_user_positions(wallet)
        positions = normalize_positions(raw)

        for p in positions:
            p["wallet"] = wallet
            all_positions.append(p)

    return all_positions


# ---------------------------
# CORE CONSENSUS ENGINE
# ---------------------------
def compute_consensus(positions, wallet_count):

    # FIRST LEVEL: strict canonical aggregation
    markets = {}

    for p in positions:
        raw_market = p.get("market", "")
        market = normalize_market_name(raw_market)

        side = p.get("side", "YES").upper()
        wallet = p.get("wallet")

        if market not in markets:
            markets[market] = {
                "YES": set(),
                "NO": set(),
                "wallets": set(),
                "size": 0
            }

        markets[market][side].add(wallet)
        markets[market]["wallets"].add(wallet)
        markets[market]["size"] += float(p.get("size", 0) or 0)

    # SECOND LEVEL: scoring
    results = []

    for market, data in markets.items():
        yes_count = len(data["YES"])
        no_count = len(data["NO"])
        total_wallets = len(data["wallets"])

        if wallet_count == 0:
            continue

        direction = "YES" if yes_count >= no_count else "NO"

        # more realistic scoring spread
        agreement = max(yes_count, no_count) / wallet_count
        participation = total_wallets / wallet_count

        strength = (
            (agreement * 0.65) +
            (participation * 0.35)
        ) * 100

        results.append({
            "market": market,
            "direction": direction,
            "yes_count": yes_count,
            "no_count": no_count,
            "wallet_count": total_wallets,
            "strength": round(strength, 1)
        })

    # sort
    results.sort(key=lambda x: x["strength"], reverse=True)

    return results


# ---------------------------
# ENTRY POINT
# ---------------------------
def get_top_consensus(wallets_5, wallets_25):

    five_positions = build_wallet_snapshot(wallets_5)
    top_positions = build_wallet_snapshot(wallets_25)

    five = compute_consensus(five_positions, len(wallets_5))
    top25 = compute_consensus(top_positions, len(wallets_25))

    return five, top25
