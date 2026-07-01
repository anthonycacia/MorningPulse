import httpx
from datetime import date, timedelta
from app.core.utils import chunk_list
from app.services.fx_cache import set_cache
from app.core.logging import logger


class FXProvider:
    BASE_URL = "https://fxmarketapi.com/apitimeseries"


    def __init__(self, api_key: str):
        self.api_key = api_key


    @staticmethod
    def _adjust_to_weekday(d: date) -> date:
        while d.weekday() >= 5:
            d -= timedelta(days=1)
        return d


    def get_last_trading_day(self):
        return self._adjust_to_weekday(date.today() - timedelta(days=1))


    async def fetch(self, currencies: list[str], days: int = 150):
        if isinstance(currencies, str):
            raise ValueError("currencies must be list[str], got str. Did you forget .split(',')?")
        
        end_date = self.get_last_trading_day()
        start_date = self._adjust_to_weekday(end_date - timedelta(days=days))

        all_data = {}

        async with httpx.AsyncClient(timeout=10) as client:
            for group in chunk_list(currencies, 3):

                params = {
                    "api_key": self.api_key,
                    "currency": ",".join(group),
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "interval": "daily",
                    "format": "close",
                }
                
                logger.info("Fetching FX data")

                r = await client.get(self.BASE_URL, params=params)
                r.raise_for_status()
                data = r.json()

                if "price" not in data:
                    logger.error("Batch failed: %s %s", group, data)
                    continue

                for day, values in data["price"].items():
                    all_data.setdefault(day, {})
                    all_data[day].update(values)

        if not all_data:
            logger.error("No FX data received from API")
            raise RuntimeError("FX API returned no price data")

        set_cache({"price": all_data})
        logger.info("Loaded cache")                     
        return {"price": all_data}