"""
Script para iniciar una llamada con el agente de IA
"""
import os
from twilio.rest import Client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Credenciales de Twilio
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_PHONE_NUMBER')
to_number = os.getenv('TO_PHONE_NUMBER')  # Número al que llamar

# URL de tu servidor (debe ser accesible públicamente)
# En desarrollo local: usar ngrok (ngrok http 5000)
# En producción: URL de tu app en Railway/Render/Heroku
webhook_url = os.getenv('WEBHOOK_URL')

if not webhook_url:
    print("❌ ERROR: WEBHOOK_URL no está configurado en .env")
    print("   Para desarrollo local: ngrok http 5000")
    print("   Para producción: URL de tu app desplegada")
    exit(1)

# Asegurar que la URL termine con /voice
if not webhook_url.endswith('/voice'):
    if webhook_url.endswith('/'):
        webhook_url = webhook_url + 'voice'
    else:
        webhook_url = webhook_url + '/voice'

client = Client(account_sid, auth_token)

print(f"📞 Iniciando llamada a {to_number}...")
print(f"🔗 Webhook: {webhook_url}")

call = client.calls.create(
    url=webhook_url,
    to=to_number,
    from_=twilio_number,
    status_callback=webhook_url.replace('/voice', '/status'),
    status_callback_event=['initiated', 'ringing', 'answered', 'completed']
)

print(f"✅ Llamada iniciada. SID: {call.sid}")
print(f"📊 Estado: {call.status}")
