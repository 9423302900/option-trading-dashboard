import yaml
import pandas as pd
from datetime import datetime
from data.fetch_nse_data import fetch_option_chain
import ta

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def add_adx(df):
    df['ADX'] = ta.trend.adx(df['high'], df['low'], df['close'], window=14)
    return df

def add_vwap(df):
    df['VWAP'] = (df['close'] * df['volume']).cumsum() / df['volume'].cumsum()
    return df

def load_config():
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)

def generate_signals():
    config = load_config()
    alerts = []

    for symbol in config.get("indices", []):
        data = fetch_option_chain(symbol)
        if not data:
            continue

        spot = data["records"]["underlyingValue"]
        atm = min(data["records"]["data"], key=lambda x: abs(x["strikePrice"] - spot))
        ce = atm.get("CE", {})
        if not ce:
            continue

        # Dummy close prices for RSI
        df = pd.DataFrame({"close": [ce["lastPrice"]] * 20})
        rsi = calculate_rsi(df["close"]).iloc[-1]

        if rsi < 35:
            entry = ce["lastPrice"]
            sl = entry - 20
            tgt = entry + 1.5 * (entry - sl)
            msg = (
                f"📢 Buy Signal – {symbol}\n"
                f"🔹 Strike: {ce['strikePrice']} CE\n"
                f"💰 Entry: ₹{entry}\n"
                f"🛑 SL: ₹{sl} 🎯 Target: ₹{tgt}\n"
                f"RSI: {round(rsi, 2)} ⏱ {datetime.now().strftime('%H:%M:%S')}"
            )
            alerts.append({"message": msg})

    return alerts
