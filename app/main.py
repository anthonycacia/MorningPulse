from dotenv import load_dotenv

load_dotenv()

import httpx
from app.discord.client import DiscordNotifier
from app.providers.fxmarketapi import FXProvider
from app.services.fx_cache import get_mock_fx_data
from app.services.morning_pulse import (
    generate_fx_message,
    normalize_source,
    resolve_fx_data,
)
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from app.core.config import forex_pairs, FOREX_API_KEY, DISCORD_WEBHOOK_URL


app = FastAPI(title="MorningPulse", version="0.1.0")

symbols = forex_pairs()


@app.middleware("http")
async def disable_docs_cache(request: Request, call_next):
    response = await call_next(request)
    if request.url.path in ("/docs", "/openapi.json", "/redoc"):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        response.headers["Pragma"] = "no-cache"
    return response


@app.exception_handler(httpx.HTTPStatusError)
async def upstream_http_error(request: Request, exc: httpx.HTTPStatusError):
    url = str(exc.request.url)
    if "fxmarketapi.com" in url:
        detail = "FX API request failed. Check FOREX_API_KEY in .env and rebuild with docker compose up --build."
    elif "discord.com" in url:
        detail = "Discord webhook request failed. Check DISCORD_WEBHOOK_URL in .env."
    else:
        detail = f"Upstream request failed with HTTP {exc.response.status_code}."

    return JSONResponse(status_code=502, content={"detail": detail})


# -------------------------
# Dependency wiring
# -------------------------

if not FOREX_API_KEY:
    raise RuntimeError("FOREX_API_KEY not set")

if not DISCORD_WEBHOOK_URL:
    raise RuntimeError("DISCORD_WEBHOOK_URL not set")

fx_provider = FXProvider(
    api_key=FOREX_API_KEY
)

discord_notifier = DiscordNotifier(
    webhook_url=DISCORD_WEBHOOK_URL
)


# -------------------------
# Health check
# -------------------------

@app.get("/health/live")
async def health_live():
    return {
        "status": "alive"
    }


@app.get("/health/ready")
async def health_ready():
    checks = {
        "forex_api_configured": bool(FOREX_API_KEY),
        "discord_configured": bool(DISCORD_WEBHOOK_URL),
    }

    return {
        "status": "ready" if all(checks.values()) else "not_ready",
        "checks": checks,
    }


@app.get("/msg")
async def msg(
    source: str = Query(
        default="auto",
        description="auto: cache if present else API; cache: disk only; api: live API; mock: fixture data",
    ),
):
    resolved = normalize_source(source)
    message, resolved_source = await generate_fx_message(fx_provider, symbols, resolved)

    return {
        "source": resolved_source,
        "message": message,
    }


@app.get("/debug/fx")
async def debug_fx(
    source: str = Query(
        default="auto",
        description="auto: cache if present else API; cache: disk only; api: live API; mock: fixture data",
    ),
):
    resolved = normalize_source(source)
    data, resolved_source = await resolve_fx_data(fx_provider, symbols, resolved)

    return {
        "source": resolved_source,
        "data": data,
    }


@app.get("/debug/fx/mock")
async def fx_mock():
    return get_mock_fx_data()


@app.post("/debug/fx/refresh-cache")
async def refresh_fx_cache():
    data, resolved = await resolve_fx_data(fx_provider, symbols, "api")

    return {
        "status": "ok",
        "source": resolved,
        "data": data,
    }


@app.post("/run/morning-pulse")
async def run_morning_pulse():
    message, _ = await generate_fx_message(
        fx_provider,
        symbols,
        source="api",
    )

    await discord_notifier.send(message)

    return {
        "status": "sent",
        "message": message,
    }
