raw_sample_prices = [100.0, None, 102.5, "101.0", 105.0, 108.2, None, 107.0, 110.0, 115.0]


def clean_data(data):
    cleaned = []
    for item in data:
        if item is not None:
            try:
                cleaned.append(float(item))
            except ValueError:
                continue
    return cleaned


def compute_indicators(prices, window=3):
    indicators = []
    for i in range(len(prices)):
        current_price = prices[i]
        prev_price = prices[i - 1] if i > 0 else current_price
        daily_return = ((current_price - prev_price) / prev_price) * 100

        if i >= window - 1:
            sma = sum(prices[i - window + 1 : i + 1]) / window
        else:
            sma = None

        indicators.append({
            "price": current_price,
            "daily_return_%": round(daily_return, 2),
            "sma": round(sma, 2) if sma else None,
        })
    return indicators


def analyze(indicators):
    prices = [item["price"] for item in indicators]
    total_change = ((prices[-1] - prices[0]) / prices[0]) * 100
    return {
        "start_price": prices[0],
        "end_price": prices[-1],
        "highest": max(prices),
        "lowest": min(prices),
        "total_return_%": round(total_change, 2),
    }


def generate_signals(indicators):
    signals = []
    for item in indicators:
        price = item["price"]
        sma = item["sma"]

        if sma is None:
            signal = "HOLD (Warming up)"
        elif price > sma:
            signal = "BUY"
        elif price < sma:
            signal = "SELL"
        else:
            signal = "HOLD"

        signals.append({"price": price, "sma": sma, "signal": signal})
    return signals

def create_report(analysis, signals):
    print("=" * 48)
    print("           DAILY STOCK MARKET REPORT            ")
    print("=" * 48)
    print(f"Start Price  : ${analysis['start_price']:.2f}")
    print(f"End Price    : ${analysis['end_price']:.2f}")
    print(f"High / Low   : ${analysis['highest']:.2f} / ${analysis['lowest']:.2f}")
    print(f"Total Return : {analysis['total_return_%']}%")
    print("-" * 48)
    print("Signals Log:")
    for idx, s in enumerate(signals, 1):
        sma_val = f"${s['sma']:.2f}" if s["sma"] is not None else "N/A   "
        print(f"  Day {idx:02d} | Price: ${s['price']:<6.2f} | SMA: {sma_val} | Signal: {s['signal']}")
    print("=" * 48)

 
if __name__ == "__main__":
    cleaned = clean_data(raw_sample_prices)
    print("[✓] clean_data():", cleaned)

    indicators = compute_indicators(cleaned)
    print("[✓] compute_indicators():", indicators[:2], "...")

    summary = analyze(indicators)
    print("[✓] analyze():", summary)

    signals = generate_signals(indicators)
    print("[✓] generate_signals():", signals[:2], "...")

    print("\n[✓] create_report():")
    create_report(summary, signals)