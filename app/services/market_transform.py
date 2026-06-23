from collections import defaultdict

def to_series(price_data: dict) -> dict[str, list[float]]:
    series = defaultdict(list)

    for day in sorted(price_data.keys()):
        for symbol, value in price_data[day].items():
            series[symbol].append(value)

    return series