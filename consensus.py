from collections import defaultdict
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


def compute_consensus(positions, wallet_count):

    markets = {}

    for p in positions:

        market = p["market"]
        outcome = p["side"].upper()
        wallet = p["wallet"]
        size = float(p.get("size", 0))

        if market not in markets:
            markets[market] = {
                "wallets": set(),
                "outcomes": defaultdict(set),
                "volume": 0
            }

        markets[market]["wallets"].add(wallet)
        markets[market]["outcomes"][outcome].add(wallet)
        markets[market]["volume"] += size

    results = []

    for market, data in markets.items():

        winning_outcome = None
        winning_wallets = 0

        for outcome, wallets in data["outcomes"].items():

            if len(wallets) > winning_wallets:
                winning_wallets = len(wallets)
                winning_outcome = outcome

        strength = round(100 * winning_wallets / wallet_count, 1)

        results.append({
            "market": market,
            "direction": winning_outcome,
            "wallet_count": winning_wallets,
            "strength": strength,
            "volume": round(data["volume"], 2)
        })

    results.sort(
        key=lambda x: (
            x["strength"],
            x["volume"]
        ),
        reverse=True
    )

    return results


def get_top_consensus(wallets_5, wallets_25):

    five_positions = build_wallet_snapshot(wallets_5)
    top_positions = build_wallet_snapshot(wallets_25)

    five = compute_consensus(five_positions, len(wallets_5))
    top25 = compute_consensus(top_positions, len(wallets_25))

    return five, top25
