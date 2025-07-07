from twilio.rest import Client

def send_whatsapp_alert(message):
    account_sid = "your_twilio_sid"
    auth_token = "your_twilio_auth_token"
    from_whatsapp = "whatsapp:+14155238886"  # Twilio sandbox
    to_whatsapp = "whatsapp:+91YOURNUMBER"

    client = Client(account_sid, auth_token)
    client.messages.create(
        from_=from_whatsapp,
        body=message,
        to=to_whatsapp
    )

