import json
from pathlib import Path

CACHE_FILE = Path("/app/cache/fx_cache.json")
MOCK_FILE = Path(__file__).resolve().parent.parent / "fixtures" / "fx_mock.json"


def set_cache(data):
    CACHE_FILE.write_text(json.dumps(data))


def get_cache():
    if not CACHE_FILE.exists():
        return None
    return json.loads(CACHE_FILE.read_text())


def get_mock_fx_data():
    return json.loads(MOCK_FILE.read_text())
