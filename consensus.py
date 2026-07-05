from collections import defaultdict
from polymarket import load_wallet


def get_top_consensus(wallets_5, wallets_25):
    five_positions = []
    top25_positions = []

    for w in wallets_5:
        five_positions.extend(load_wallet(w))

    for w in wallets_25:
        top25_positions.extend(load_wallet(w))

    five = compute_consensus(five_positions, len(wallets_5))
    top25 = compute_consensus(top25_positions, len(wallets_25))

    return five, top25


def compute_consensus(positions, wallet_count):

    markets = defaultdict(lambda: {
        "YES": set(),
        "NO": set(),
        "size": 0.0
    })

    for p in positions:
        market = (p.get("market") or "").strip()
        if not market:
            continue

        side = (p.get("side") or "YES").upper()
        wallet = p.get("wallet")

        if not wallet:
            continue

        if side not in ["YES", "NO"]:
            continue

        markets[market][side].add(wallet)

        try:
            markets[market]["size"] += float(p.get("size", 0))
        except Exception:
            pass

    results = []

    for market, data in markets.items():
        yes_count = len(data["YES"])
        no_count = len(data["NO"])

        if yes_count == 0 and no_count == 0:
            continue

        if yes_count >= no_count:
            direction = "YES"
            winning_count = yes_count
        else:
            direction = "NO"
            winning_count = no_count

        strength = (winning_count / wallet_count) * 100
        participating_wallets = len(data["YES"] | data["NO"])

        results.append({
            "market": market,
            "direction": direction,
            "strength": round(strength, 1),
            "volume": round(data["size"], 2),
            "wallets": participating_wallets,
            "total_wallets": wallet_count,
            "yes_count": yes_count,
            "no_count": no_count,
        })

    results.sort(key=lambda x: (x["strength"], x["wallets"], x["volume"]), reverse=True)

    return results[:10]
