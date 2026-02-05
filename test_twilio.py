# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Set environment variables for your credentials
# Read more at http://twil.io/secure

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

if not account_sid or not auth_token:
    raise ValueError("TWILIO_ACCOUNT_SID y TWILIO_AUTH_TOKEN deben estar configurados en .env")
client = Client(account_sid, auth_token)

# Crear respuesta TwiML con texto y lenguaje personalizados
response = VoiceResponse()
# language: código de idioma (es-ES para español de España, es-MX para México, en-US para inglés, etc.)
# voice: tipo de voz (alice, man, woman, etc.)
response.say(
    "Hola, esta es una llamada de prueba desde Twilio. Gracias por tu atención.",
    language='es-ES',
    voice='alice'
)

# Realizar la llamada usando TwiML directamente
call = client.calls.create(
    twiml=response.to_xml(),  # Usar twiml en lugar de url
    to="+34602074744",
    from_="+18564926544"
)

print(call.sid)