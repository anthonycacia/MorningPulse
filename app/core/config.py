import os
from dotenv import load_dotenv

load_dotenv()


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