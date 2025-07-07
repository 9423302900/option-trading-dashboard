from datetime import datetime

def get_signals():
    # Simulate one dummy signal for BANKNIFTY
    now = datetime.now().strftime("%H:%M:%S")
    signal = {
        "symbol": "BANKNIFTY",
        "strike": "49500 CE",
        "entry": 125,
        "sl": 105,
        "target": 165,
        "message": f"📢 Buy Signal – BANKNIFTY\n📈 Entry: 49500 CE @ ₹125\n🛑 SL: ₹105 🎯 Target: ₹165\n⏱ Time: {now}"
    }
    return [signal]

