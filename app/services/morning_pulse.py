from app.services.fx_cache import get_cache
from app.services.market_transform import to_series
from app.services.report import build_morning_message


async def generate_fx_message(
    fx_provider,
    symbols
):
    cache = get_cache()
    if cache:
        data = cache
    else:
        data = await fx_provider.fetch(symbols)
        
    fx_series = to_series(data["price"])

    return build_morning_message(fx_series)