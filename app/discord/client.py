import httpx
from app.core.logging import logger


class DiscordNotifier:
    def __init__(self, webhook_url: str):
        self.url = webhook_url

    async def send(self, message: str):
        async with httpx.AsyncClient() as client:
            try:
                await client.post(self.url, json={"content": message})
            except:
                logger.error("Discord send failed")
                