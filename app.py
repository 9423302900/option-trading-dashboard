import streamlit as st
from strategy.signal_logic import get_signals
from alerts.whatsapp import send_whatsapp_alert

st.set_page_config(layout="wide")
st.title("📊 Automated Option Trading Signals – India")

signals = get_signals()

for sig in signals:
    st.success(sig['message'])
    send_whatsapp_alert(sig['message'])  # Sends to WhatsApp

import streamlit as st
from strategy.signal_logic import generate_signals

st.set_page_config(layout="wide")
st.title("📊 Option Trading Signal Dashboard – Live")

signals = generate_signals()

if not signals:
    st.warning("No signals generated yet. Try again later.")
else:
    for sig in signals:
        st.success(sig["message"])
