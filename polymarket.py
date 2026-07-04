import requests

BASE_URL = "https://data-api.polymarket.com"


def get_user_positions(wallet_address):
    """
    Fetch current positions for one wallet.
    """

    url = f"{BASE_URL}/positions?user={wallet_address}"

    print(f"\nRequesting:")
    print(url)

    try:
        response = requests.get(url, timeout=20)

        print(f"HTTP Status: {response.status_code}")

        print("\nFirst 500 characters returned:")
        print(response.text[:500])

        if response.status_code != 200:
            return []

        return response.json()

    except Exception as e:
        print(e)
        return []


def normalize_positions(raw):
    """
    We are NOT parsing anything yet.
    Just return the raw data unchanged.
    """

    return raw
