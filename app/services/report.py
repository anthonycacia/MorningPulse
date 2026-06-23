from app.core.config import forex_pairs, PAIR_NAMES, FOREX_SHORT_MOVING_AVG, FOREX_LONG_MOVING_AVG
from app.services.greetings import morning_greeting
from app.services.metrics import (
    latest,
    yesterday,
    avg,
    change,
    direction,
)
from dotenv import load_dotenv
import os
load_dotenv()


def build_morning_message(
    fx_series: dict,
    short_window: int = int(FOREX_SHORT_MOVING_AVG),
    long_window: int = int(FOREX_LONG_MOVING_AVG),
):
    message = morning_greeting()
    message += "\n\n-- MorningPulse FX Report --\n"

    pairs = forex_pairs()
    
    for pair in pairs:
        series = fx_series.get(pair)

        if not series or len(series) < 2:
            message += f"\n**{PAIR_NAMES.get(pair, pair)}:** NO DATA\n"
            continue

        today = latest(series)
        prev = yesterday(series)
        delta = change(today, prev)
        
        pct_change = (delta / prev) * 100

        short_avg = avg(series, short_window)
        long_avg = avg(series, long_window)
        long_pct = ((today - long_avg) / long_avg) * 100
        position = "ABOVE" if long_pct > 0 else "BELOW"
         
        message += f"\n**1 {PAIR_NAMES.get(pair, pair)} ({pair}):** ${today:.3f}\n"
        
        message += "\n"
        message += f"{direction(delta)}\n"
        message += f"{delta:+.3f} ({pct_change:+.2f}%)\n"      
        
        message += "\n"
        message += f"{str(short_window)}d avg: ${short_avg:.3f}\n"
        message += f"{str(long_window)}d avg: ${long_avg:.3f}\n"
        
        message += "\n"
        message += f"{abs(long_pct):.2f}% {position} long-term average\n"

    return message
