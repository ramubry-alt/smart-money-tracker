import requests

BASE_URL = "https://data-api.polymarket.com"


def get_user_positions(wallet_address):
    """
    Downloads every open position for one wallet.
    """

    url = f"{BASE_URL}/positions?user={wallet_address}"

    try:
        response = requests.get(url, timeout=20)

        if response.status_code != 200:
            return []

        return response.json()

    except Exception as e:
        print(e)
        return []


def normalize_positions(raw, wallet):
    """
    Convert Polymarket API output into one standard format.
    """

    positions = []

    for p in raw:

        try:

            title = p.get("title", "").strip()

            if not title:
                continue

            side = str(
                p.get("side")
                or p.get("outcome")
                or "YES"
            ).upper()

            try:
                size = float(p.get("size", 0))
            except Exception:
                size = 0.0

            positions.append(
                {
                    "wallet": wallet,
                    "market": title,
                    "side": side,
                    "size": size,
                }
            )

        except Exception:
            continue

    return positions


def load_wallet(wallet):
    """
    Convenience wrapper.
    """

    raw = get_user_positions(wallet)

    return normalize_positions(raw, wallet)
