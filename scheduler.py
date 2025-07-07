import schedule
import time
from strategy.signal_logic import generate_signals
from alerts.telegram import send_telegram_alert
from alerts.logger import log_alert

def job():
    print("📡 Checking for signals...")
    signals = generate_signals()
    for sig in signals:
        symbol = "BANKNIFTY"  # or parse from message
        log_alert(symbol, sig["message"])
        send_telegram_alert(sig["message"])

schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

