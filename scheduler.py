import schedule
import time
from strategy.signal_logic import get_signals
from alerts.whatsapp import send_whatsapp_alert

def job():
    print("📡 Checking for signals...")
    signals = get_signals()
    for sig in signals:
        print("🚨 Sending Signal:")
        print(sig['message'])
        send_whatsapp_alert(sig['message'])

# Run every 5 minutes
schedule.every(5).minutes.do(job)

print("🔄 Scheduler started. Running every 5 minutes...")
while True:
    schedule.run_pending()
    time.sleep(1)

