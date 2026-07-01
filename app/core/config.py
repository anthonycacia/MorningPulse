import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
FOREX_API_KEY = os.getenv("FOREX_API_KEY")

FOREX_SHORT_MOVING_AVG = int(os.getenv("FOREX_SHORT_MOVING_AVG", "42"))
FOREX_LONG_MOVING_AVG = int(os.getenv("FOREX_LONG_MOVING_AVG", "150"))

MY_NAME = os.getenv("MY_NAME", "World")

PAIR_NAMES = {
    "EURUSD": "Euro",
    "GBPUSD": "British Pound",
    "CADUSD": "Canadian Dollar",
    "AUDUSD": "Australian Dollar",
    "NZDUSD": "New Zealand Dollar",
    "USDJPY": "Japanese Yen",
    "USDCHF": "Swiss Franc",
}


def forex_pairs():
    return [
        s.strip()
        for s in os.getenv("FOREX_PAIRS", "").split(",")
        if s.strip()
    ]