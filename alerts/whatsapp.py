from twilio.rest import Client

def send_whatsapp_alert(message):
    account_sid = "HXb5b62575e6e4ff6129ad7c8efe1f983e'"
    auth_token = "A"
    from_whatsapp = "whatsapp:+14155238886"  # Twilio sandbox
    to_whatsapp = "whatsapp:+919423302900"

    client = Client(account_sid, auth_token)
    client.messages.create(
        from_=from_whatsapp,
        body=message,
        to=to_whatsapp
    )

