from collections import defaultdict
from polymarket import get_user_positions, normalize_positions


def build_wallet_snapshot(wallets):
    """
    Pulls all wallet positions and flattens them into a unified structure.
    """
    all_positions = []

    for w in wallets:
        raw = get_user_positions(w)
        positions = normalize_positions(raw)

        for p in positions:
            p["wallet"] = w
            all_positions.append(p)

    return all_positions


def compute_consensus(positions, wallet_count):
    """
    Returns consensus by market:
    - YES count
    - NO count
    - total size
    - wallets involved
    """

    markets = defaultdict(lambda: {
        "YES": set(),
        "NO": set(),
        "size": 0,
        "wallets": set()
    })

    for p in positions:
        market = p["market"]
        side = p["side"]
        wallet = p["wallet"]

        markets[market][side].add(wallet)
        markets[market]["wallets"].add(wallet)
        markets[market]["size"] += p["size"]

    results = []

    for market, data in markets.items():
        yes_count = len(data["YES"])
        no_count = len(data["NO"])
        total_wallets = len(data["wallets"])

        # determine direction
        if yes_count > no_count:
            direction = "YES"
            strength = yes_count / wallet_count
        else:
            direction = "NO"
            strength = no_count / wallet_count

        results.append({
            "market": market,
            "market_id": market,
            "direction": direction,
            "yes_count": yes_count,
            "no_count": no_count,
            "wallet_coverage": total_wallets,
            "strength": round(strength * 100, 1),
            "total_size": f"{yes_count}/{wallet_count} wallets"
        })

    # sort by strongest conviction
    results.sort(key=lambda x: x["strength"], reverse=True)

    return results


def get_top_consensus(wallets_5, wallets_25):
    """
    Builds:
    - 5-wallet consensus
    - Top 25 consensus
    """

    five_positions = build_wallet_snapshot(wallets_5)
    top_positions = build_wallet_snapshot(wallets_25)

    five = compute_consensus(five_positions, len(wallets_5))
    top25 = compute_consensus(top_positions, len(wallets_25))

    return five, top25
