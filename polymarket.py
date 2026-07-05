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


def normalize_positions(raw, wallet=None):

    from pprint import pprint

    print("\n====================================")
    print("FIRST POSITION RETURNED BY POLYMARKET")
    print("====================================\n")

    if len(raw) > 0:
        pprint(raw[0])
    else:
        print("No positions returned.")

    # Stop the program immediately
    raise SystemExit

  
    
def load_wallet(wallet):
    """
    Convenience wrapper.
    """

    raw = get_user_positions(wallet)

    return normalize_positions(raw, wallet)
