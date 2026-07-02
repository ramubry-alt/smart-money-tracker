import requests

BASE_URL = "https://gamma-api.polymarket.com"


def get_user_positions(wallet_address):
    try:
        url = f"{BASE_URL}/events?user={wallet_address}"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception:
        return []


def normalize_positions(raw):
    positions = []

    for item in raw:
        try:
            market = item.get("title") or item.get("question") or ""
            market_lower = market.lower()

            # ---------------------------
            # FILTER 1: OLD MARKETS
            # ---------------------------
            if any(x in market_lower for x in ["2020", "2021", "2022"]):
                continue

            # ---------------------------
            # FILTER 2: SPORTS NOISE
            # ---------------------------
            if any(x in market_lower for x in [
                "nba", "nfl", "mlb", "nhl",
                "beat the spread", "points",
                "touchdowns", "matchup",
                "game", "week"
            ]):
                continue

            # ---------------------------
            # FILTER 3: ENTERTAINMENT NOISE
            # ---------------------------
            if any(x in market_lower for x in [
                "gross more than",
                "opening weekend",
                "box office"
            ]) and "million" in market_lower:
                continue

            # ---------------------------
            # SIZE CALCULATION
            # ---------------------------
            size = 0

            if isinstance(item.get("outcomePositions"), list):
                for op in item["outcomePositions"]:
                    try:
                        size += float(op.get("size", 0) or 0)
                    except Exception:
                        pass

            # ---------------------------
            # SIDE NORMALIZATION
            # ---------------------------
            side = item.get("side") or item.get("outcome") or "YES"

            positions.append({
                "market": market,
                "side": str(side).upper(),
                "size": round(size, 2)
            })

        except Exception:
            continue

    return positions
