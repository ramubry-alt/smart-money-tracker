from collections import defaultdict
import re
from polymarket import get_user_positions, normalize_positions


def build_wallet_snapshot(wallets):
    all_positions = []

    for wallet in wallets:
        raw = get_user_positions(wallet)
        positions = normalize_positions(raw)

        for p in positions:
            p["wallet"] = wallet
            all_positions.append(p)

    return all_positions


def normalize_market_name(market):
    """
    Strong canonicalization to prevent duplicates.
    """
    market = market.lower().strip()

    # remove punctuation
    market = re.sub(r"[^a-z0-9\s]", "", market)

    # normalize whitespace
    market = re.sub(r"\s+", " ", market)

    return market


def compute_consensus(positions, wallet_count):
    markets = defaultdict(lambda: {
        "YES": set(),
        "NO": set(),
        "wallets": set(),
        "size": 0
    })

    for p in positions:
        raw_market = p.get("market", "")
        market = normalize_market_name(raw_market)

        side = p.get("side", "YES").upper()
        wallet = p.get("wallet")

        markets[market][side].add(wallet)
        markets[market]["wallets"].add(wallet)
        markets[market]["size"] += float(p.get("size", 0) or 0)

    results = []

    for market, data in markets.items():
        yes_count = len(data["YES"])
        no_count = len(data["NO"])
        total_wallets = len(data["wallets"])

        if wallet_count == 0:
            continue

        direction = "YES" if yes_count >= no_count else "NO"

        confidence = max(yes_count, no_count) / wallet_count
        breadth = total_wallets / wallet_count

        strength = (confidence * 0.6 + breadth * 0.4) * 100

        results.append({
            "market": market,
            "direction": direction,
            "yes_count": yes_count,
            "no_count": no_count,
            "wallet_count": total_wallets,
            "strength": round(strength, 1)
        })

    # sort by strength
    results.sort(key=lambda x: x["strength"], reverse=True)

    # final dedup safety pass
    seen = set()
    unique_results = []

    for r in results:
        if r["market"] in seen:
            continue
        seen.add(r["market"])
        unique_results.append(r)

    return unique_results


def get_top_consensus(wallets_5, wallets_25):
    five_positions = build_wallet_snapshot(wallets_5)
    top_positions = build_wallet_snapshot(wallets_25)

    five = compute_consensus(five_positions, len(wallets_5))
    top25 = compute_consensus(top_positions, len(wallets_25))

    return five, top25
