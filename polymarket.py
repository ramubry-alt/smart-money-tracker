# Placeholder Polymarket integration
# (We will upgrade this to real API logic next)

def get_user_positions(wallet_address):
    return [
        {"market": "BTC > 100k by 2026", "side": "YES", "size": 120},
        {"market": "ETH ETF approved", "side": "YES", "size": 80},
        {"market": "US recession 2026", "side": "NO", "size": 50}
    ]


def normalize_positions(raw_positions):
    """
    The mock data is already normalized.
    Later we'll convert the real Polymarket API response here.
    """
    return raw_positions
