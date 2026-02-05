"""
Script para hacer llamadas con IA SIN necesidad de webhooks/ngrok
Usa TwiML directamente pero con limitaciones: no puede capturar respuestas del usuario
"""
import os
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import openai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Credenciales de Twilio
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_PHONE_NUMBER')
to_number = os.getenv('TO_PHONE_NUMBER')

client = Client(account_sid, auth_token)

# Generar mensaje inicial con IA
def get_ai_greeting():
    """Genera un saludo personalizado con IA"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente telefónico. Genera un saludo breve y amigable (máximo 2 frases)."
                },
                {
                    "role": "user",
                    "content": "Genera un saludo para una llamada telefónica"
                }
            ],
            temperature=0.7,
            max_tokens=100
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error con OpenAI: {e}")
        return "Hola, esta es una llamada de prueba desde Twilio."

# Crear respuesta TwiML con mensaje generado por IA
response = VoiceResponse()
greeting = get_ai_greeting()

response.say(
    greeting,
    language='es-ES',
    voice='alice'
)

# NOTA: Sin webhooks, no podemos capturar la respuesta del usuario
# Esta versión solo puede enviar mensajes, no tener conversación bidireccional
response.say(
    "Gracias por tu atención. ¡Hasta luego!",
    language='es-ES',
    voice='alice'
)

# Realizar la llamada usando TwiML directamente
call = client.calls.create(
    twiml=response.to_xml(),
    to=to_number,
    from_=twilio_number
)

print(f"Llamada iniciada. SID: {call.sid}")
print(f"Estado: {call.status}")
print(f"\nMensaje enviado: {greeting}")
