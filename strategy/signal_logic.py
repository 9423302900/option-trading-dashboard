from data.fetch_nse_data import fetch_option_chain

def get_signals():
    data = fetch_option_chain("BANKNIFTY")
    if not data:
        return []

    # Extracting ATM CE for simplicity
    records = data["records"]["data"]
    underlying = data["records"]["underlyingValue"]
    nearest = min(records, key=lambda x: abs(x["strikePrice"] - underlying))
    ce = nearest.get("CE", {})

    if ce:
        ltp = ce.get("lastPrice", 0)
        strike = ce.get("strikePrice", "NA")
        msg = f"📢 Live BUY – BANKNIFTY\nStrike: {strike} CE\nLTP: ₹{ltp}\n⏱ Live"
        return [{"message": msg}]
    else:
        return []
def fetch_crude_price():
    url = "https://commodityapi.com/api/latest"
    params = {
        "access_key": "YOUR_API_KEY",
        "symbols": "CRUDEOIL"
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        return res.json().get("data", {}).get("CRUDEOIL", {}).get("price", "N/A")
    return None


