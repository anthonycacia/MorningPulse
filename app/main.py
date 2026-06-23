import os
from app.discord.client import DiscordNotifier
from app.providers.fxmarketapi import FXProvider
from app.services.fx_cache import get_cache, set_cache, has_cache
from app.services.greetings import morning_greeting
from app.services.market_transform import to_series
from app.services.morning_pulse import generate_fx_message
from dotenv import load_dotenv
from fastapi import FastAPI


load_dotenv()
app = FastAPI(title="MorningPulse", version="0.1.0")

from app.core.config import forex_pairs
symbols = forex_pairs()


# -------------------------
# Dependency wiring
# -------------------------

fx_provider = FXProvider(
    api_key=os.getenv("FOREX_API_KEY", "")
)

discord_notifier = DiscordNotifier(
    webhook_url=os.getenv("DISCORD_WEBHOOK_URL", "")
)


# -------------------------
# Health check
# -------------------------

@app.get("/health")
async def health():
    checks = {
        "forex_api_configured": bool(os.getenv("FOREX_API_KEY")),
        "discord_configured": bool(os.getenv("DISCORD_WEBHOOK_URL")),
    }

    return {
        "status": "ok" if all(checks.values()) else "degraded",
        "checks": checks,
    }
    

@app.get("/msg")
async def msg():

    message = await generate_fx_message(
        fx_provider,
        symbols,
    )

    return {
        "message": message
    }

# -------------------------
# Debug FX endpoint (with optional cache)
# -------------------------

@app.get("/debug/fx")
async def debug_fx():

    if has_cache():
        return {
            "source": "cache",
            "data": get_cache()
        }

    data = await fx_provider.fetch(symbols)
    
    return {
        "source": "api",
        "data": data
    }


@app.post("/run/morning-pulse")
async def run_morning_pulse():

    # Send good morning message first
    message = await generate_fx_message(
        fx_provider,
        symbols,
    )
    
    await discord_notifier.send(message)

    return {
        "status": "sent",
        "message": message
    }