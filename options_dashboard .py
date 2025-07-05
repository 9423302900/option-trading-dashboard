
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")
st.title("💹 Option Trading Dashboard – OI, Signals & Breakouts")

# === Telegram Bot Setup ===
bot_token = "YOUR_BOT_TOKEN"
chat_id = "YOUR_CHAT_ID"

def send_telegram_alert(message, bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        requests.post(url, data=payload)
    except:
        pass

# === NSE Data Fetch ===
def fetch_oi(symbol="NIFTY"):
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.nseindia.com/",
        "Connection": "keep-alive",
        "DNT": "1"
    }
    session = requests.Session()
    for attempt in range(3):
        try:
            session.get("https://www.nseindia.com", headers=headers, timeout=5)
            response = session.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data["records"]["data"]
        except Exception as e:
            st.warning(f"⚠️ Attempt {attempt+1} failed: {e}")
    st.error(f"❌ Could not fetch data for {symbol} after 3 attempts.")
    st.stop()

def get_spot_price(symbol):
    symbol_map = {"NIFTY": "NIFTY 50", "BANKNIFTY": "NIFTY BANK"}
    url = f"https://www.nseindia.com/api/equity-stockIndices?index={symbol_map[symbol]}"
    headers = {"User-Agent": "Mozilla/5.0"}
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)
    response = session.get(url, headers=headers)
    data = response.json()
    return float(data["data"][0]["last"])

def analyze_data(records, atm, range_limit):
    signal_dict = {}
    for item in records:
        try:
            strike = item["strikePrice"]
            if abs(strike - atm) > range_limit:
                continue
            ce_oi = item["CE"]["changeinOpenInterest"]
            pe_oi = item["PE"]["changeinOpenInterest"]
            if ce_oi < 0 and pe_oi > 0:
                signal_dict[strike] = "✅ Buy CE"
            elif ce_oi > 0 and pe_oi < 0:
                signal_dict[strike] = "🔴 Buy PE"
        except:
            continue
    return signal_dict

# === Streamlit Tabs ===
tab1, tab2 = st.tabs(["📊 OI Dashboard", "🚀 Breakout Info"])

# === OI Dashboard Tab ===
with tab1:
    symbol = st.selectbox("Select Symbol", ["NIFTY", "BANKNIFTY"])
    if st.button("🔄 Refresh OI Signals"):
        st.info("📡 Fetching live data from NSE...")
        data = fetch_oi(symbol)
        spot = get_spot_price(symbol)
        range_limit = 200 if symbol == "NIFTY" else 500
        signal_dict = analyze_data(data, spot, range_limit)

        if signal_dict:
            st.success(f"📈 Signals for {symbol} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            df = pd.DataFrame(signal_dict.items(), columns=["Strike Price", "Signal"])
            st.dataframe(df)
            for strike, signal in signal_dict.items():
                msg = f"{symbol} {signal} at {strike} | {datetime.now().strftime('%H:%M:%S')}"
                send_telegram_alert(msg, bot_token, chat_id)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download CSV", csv, f"{symbol}_signals.csv", "text/csv")
        else:
            st.warning("⚠️ No signals found in current data.")

# === Breakout Info Tab ===
with tab2:
    st.subheader("💡 Basic breakout tab placeholder")
    st.write("You can manually list stocks or signals here or replace this with volume-based logic later.")
