from collections import defaultdict
from polymarket import get_user_positions, normalize_positions


def build_wallet_snapshot(wallets):
    all_positions = []

    for w in wallets:
        raw = get_user_positions(w)
        positions = normalize_positions(raw)

        for p in positions:
            p["wallet"] = w
            all_positions.append(p)

    return all_positions


def normalize_market_name(market):
    """
    Canonicalizes market names to reduce duplicates.
    """
    return market.strip().lower()


def compute_consensus(positions, wallet_count):

    markets = defaultdict(lambda: {
        "YES": set(),
        "NO": set(),
        "wallets": set(),
        "size": 0
    })

    for p in positions:
        market = normalize_market_name(p["market"])
        side = p["side"]
        wallet = p["wallet"]

        markets[market][side].add(wallet)
        markets[market]["wallets"].add(wallet)
        markets[market]["size"] += p.get("size", 0)

    results = []

    for market, data in markets.items():
        yes_count = len(data["YES"])
        no_count = len(data["NO"])
        total_wallets = len(data["wallets"])

        if wallet_count == 0:
            continue

        # directional confidence (not saturated)
        direction = "YES" if yes_count >= no_count else "NO"

        confidence = max(yes_count, no_count) / wallet_count
        breadth = total_wallets / wallet_count

        # smoother scoring (prevents 100% flattening)
        strength = (confidence * 0.6 + breadth * 0.4) * 100

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

    # final dedup pass (safety layer)
    seen = set()
    unique = []

    for r in results:
        key = r["market"]
        if key in seen:
            continue
        seen.add(key)
        unique.append(r)

    return unique


def get_top_consensus(wallets_5, wallets_25):
    five_positions = build_wallet_snapshot(wallets_5)
    top_positions = build_wallet_snapshot(wallets_25)

    five = compute_consensus(five_positions, len(wallets_5))
    top25 = compute_consensus(top_positions, len(wallets_25))

    return five, top25
