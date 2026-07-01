from typing import Literal

from fastapi import HTTPException

from app.services.fx_cache import get_cache, get_mock_fx_data
from app.services.market_transform import to_series
from app.services.report import build_morning_message

FxSource = Literal["auto", "cache", "api", "mock"]


def normalize_source(source: str) -> FxSource:
    if not source:
        return "auto"
    if source not in ("auto", "cache", "api", "mock"):
        raise HTTPException(
            status_code=422,
            detail="source must be auto, cache, api, or mock",
        )
    return source


async def resolve_fx_data(fx_provider, symbols, source: FxSource = "auto"):
    if source == "mock":
        return get_mock_fx_data(), "mock"

    if source == "cache":
        cache = get_cache()
        if not cache:
            raise HTTPException(
                status_code=404,
                detail="No FX cache on disk. Populate with POST /debug/fx/refresh-cache or GET /debug/fx?source=api",
            )
        return cache, "cache"

    if source == "auto":
        cache = get_cache()
        if cache:
            return cache, "cache"

    data = await fx_provider.fetch(symbols)
    return data, "api"


async def generate_fx_message(fx_provider, symbols, source: FxSource = "auto"):
    data, resolved = await resolve_fx_data(fx_provider, symbols, source)
    fx_series = to_series(data["price"])
    return build_morning_message(fx_series), resolved
