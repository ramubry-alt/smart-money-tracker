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


def compute_consensus(positions, wallet_count):

    markets = defaultdict(lambda: {
        "YES": set(),
        "NO": set(),
        "wallets": set(),
        "size": 0
    })

    for p in positions:
        market = p["market"].strip()
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

        # avoid zero division safety
        if wallet_count == 0:
            continue

        if yes_count >= no_count:
            direction = "YES"
            base_strength = yes_count / wallet_count
        else:
            direction = "NO"
            base_strength = no_count / wallet_count

        # improved scoring: reward breadth + participation
        breadth = total_wallets / wallet_count
        strength = (base_strength * 0.7 + breadth * 0.3) * 100

        results.append({
            "market": market,
            "direction": direction,
            "yes_count": yes_count,
            "no_count": no_count,
            "wallet_count": total_wallets,
            "strength": round(strength, 1)
        })

    # ---------------------------
    # DEDUP + FINAL SORT
    # ---------------------------
    seen = set()
    unique_results = []

    for r in sorted(results, key=lambda x: x["strength"], reverse=True):
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
