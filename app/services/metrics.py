from statistics import mean


def latest(values):
    return values[-1] if values else None


def yesterday(values):
    return values[-2] if len(values) >= 2 else None


def avg(values, window: int):
    if not values:
        return None
    windowed = values[-window:] if len(values) >= window else values
    return mean(windowed)


def change(today, yesterday):
    if today is None or yesterday is None:
        return None
    return today - yesterday


def direction(change_value):
    if change_value is None:
        return "⚪ NO DATA"

    if change_value > 0:
        return "📈 UP from yesterday"

    if change_value < 0:
        return "📉 DOWN from yesterday"

    return "➡️ EQUAL to yesterday"
