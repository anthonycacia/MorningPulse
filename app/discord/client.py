import httpx


class DiscordNotifier:
    def __init__(self, webhook_url: str):
        self.url = webhook_url

    async def send(self, message: str):
        async with httpx.AsyncClient() as client:
            r = await client.post(self.url, json={"content": message})
            r.raise_for_status()
