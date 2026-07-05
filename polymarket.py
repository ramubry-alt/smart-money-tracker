import json
from datetime import date, datetime
from urllib.request import Request
from urllib.request import urlopen

try:
    import requests
except ImportError:
    requests = None

BASE_URL = "https://data-api.polymarket.com"


def get_user_positions(wallet_address):
    """
    Downloads every open position for one wallet.
    """

    url = f"{BASE_URL}/positions?user={wallet_address}"

    try:
        if requests is not None:
            response = requests.get(
                url,
                timeout=20,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            if response.status_code != 200:
                return []

            return response.json()

        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})

        with urlopen(request, timeout=20) as response:
            if response.status != 200:
                return []

            return json.loads(response.read().decode("utf-8"))

    except Exception as e:
        print(e)
        return []


def parse_date(value):
    if not value:
        return None

    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).date()
    except Exception:
        return None


def is_active_market(item):
    """
    Removes expired or redeemable markets.
    """

    if item.get("redeemable") is True:
        return False

    end_date = parse_date(item.get("endDate"))

    if end_date is not None and end_date < date.today():
        return False

    return True


def is_quality_market(market, item=None):
    market_lower = market.lower()
    item = item or {}

    slug_text = " ".join([
        str(item.get("slug") or ""),
        str(item.get("eventSlug") or ""),
        str(item.get("icon") or ""),
    ]).lower()

    if len(market.strip()) < 15:
        return False

    if any(x in market_lower for x in ["2020", "2021", "2022"]):
        return False

    if any(x in market_lower for x in [
        "beat the spread",
    ]):
        return False

    if any(x in slug_text for x in [
        "test-market",
    ]):
        return False

    if any(x in market_lower for x in [
        "gross more than",
        "opening weekend",
        "box office",
    ]) and "million" in market_lower:
        return False

    return True


def normalize_positions(raw, wallet=None):
    positions = []

    for item in raw:
        try:
            if not is_active_market(item):
                continue

            market = (
                item.get("title")
                or item.get("question")
                or item.get("market")
                or item.get("eventTitle")
                or ""
            ).strip()

            if not market:
                continue

            if not is_quality_market(market, item):
                continue

            side = (
                item.get("side")
                or item.get("outcome")
                or item.get("outcomeName")
                or "YES"
            )
            side = str(side).upper()

            if side not in ["YES", "NO"]:
                continue

            size = (
                item.get("currentValue")
                or item.get("initialValue")
                or item.get("size")
                or item.get("value")
                or item.get("amount")
                or 0
            )

            positions.append({
                "market": market,
                "side": side,
                "size": round(float(size or 0), 2),
                "wallet": wallet,
            })

        except Exception:
            continue

    return positions


def load_wallet(wallet):
    """
    Convenience wrapper.
    """

    raw = get_user_positions(wallet)

    return normalize_positions(raw, wallet)
