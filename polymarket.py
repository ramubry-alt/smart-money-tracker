import requests
from datetime import datetime, timezone

BASE_URL = "https://data-api.polymarket.com"


def get_user_positions(wallet_address):
    """
    Fetch CURRENT OPEN positions for a wallet.
    """
    try:
        url = f"{BASE_URL}/positions"

        params = {
            "user": wallet_address,
            "sizeThreshold": 1,
            "limit": 500
        }

        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()

        return r.json()

    except Exception as e:
        print(f"Error fetching {wallet_address}: {e}")
        return []


def normalize_positions(raw):
    positions = []

    today = datetime.now(timezone.utc)

    for item in raw:

        try:
            title = item.get("title", "").strip()

            if not title:
                continue

            # Skip tiny positions
            size = float(item.get("size", 0))

            if size < 1:
                continue

            # Skip expired markets
            end_date = item.get("endDate")

            if end_date:
                try:
                    end = datetime.fromisoformat(
                        end_date.replace("Z", "+00:00")
                    )

                    if end < today:
                        continue

                except Exception:
                    pass

            positions.append({
                "market": title,
                "side": item.get("outcome", "YES").upper(),
                "size": round(size, 2)
            })

        except Exception:
            continue

    return positions
