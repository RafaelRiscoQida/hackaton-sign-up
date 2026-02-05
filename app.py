"""
Servidor Flask para integrar Twilio con un agente de IA conversacional
"""
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
import openai
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configurar OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Almacenar el contexto de conversación por llamada
# En producción, usar Redis o una base de datos
conversations = {}


def get_ai_response(user_message, call_sid):
    """
    Obtiene respuesta del agente de IA basado en el mensaje del usuario
    """
    # Obtener historial de conversación
    if call_sid not in conversations:
        conversations[call_sid] = []
    
    # Agregar mensaje del usuario al historial
    conversations[call_sid].append({"role": "user", "content": user_message})
    
    # Preparar mensajes para OpenAI (incluir historial)
    messages = [
        {
            "role": "system",
            "content": "Eres un asistente telefónico amigable y profesional. Responde de forma concisa y natural, como si estuvieras hablando por teléfono. Mantén las respuestas breves (máximo 2-3 frases)."
        }
    ]
    messages.extend(conversations[call_sid][-10:])  # Últimos 10 mensajes para contexto
    
    try:
        # Llamar a OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # o "gpt-4" si tienes acceso
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )
        
        ai_message = response.choices[0].message.content
        
        # Agregar respuesta de IA al historial
        conversations[call_sid].append({"role": "assistant", "content": ai_message})
        
        return ai_message
    except Exception as e:
        print(f"Error con OpenAI: {e}")
        return "Lo siento, hubo un error al procesar tu mensaje. ¿Puedes repetirlo?"


@app.route('/voice', methods=['POST'])
def voice():
    """
    Endpoint inicial cuando se recibe una llamada
    """
    call_sid = request.form.get('CallSid')
    print(f"[{call_sid}] Llamada recibida")
    
    response = VoiceResponse()
    
    # Saludo inicial
    response.say(
        "Hola, soy tu asistente de IA. ¿En qué puedo ayudarte hoy?",
        language='es-ES',
        voice='alice'
    )
    
    # Redirigir a gather para capturar la respuesta del usuario
    response.redirect('/gather', method='POST')
    
    return str(response)


@app.route('/gather', methods=['POST'])
def gather():
    """
    Captura la entrada de voz del usuario y procesa con IA
    """
    response = VoiceResponse()
    call_sid = request.form.get('CallSid')
    
    # Obtener el texto transcrito del usuario
    speech_result = request.form.get('SpeechResult', '')
    
    if speech_result:
        print(f"[{call_sid}] Usuario dijo: {speech_result}")
        
        # Procesar con IA
        ai_response = get_ai_response(speech_result, call_sid)
        print(f"[{call_sid}] IA respondió: {ai_response}")
        
        # Responder con la voz de la IA
        response.say(
            ai_response,
            language='es-ES',
            voice='alice'
        )
        
        # Pausa breve antes de preguntar de nuevo
        response.pause(length=1)
    
    # Configurar Gather para capturar la siguiente respuesta del usuario
    gather = Gather(
        input='speech',
        language='es-ES',
        speech_timeout='auto',
        action='/gather',
        method='POST',
        timeout=10,  # Timeout de 10 segundos
        finish_on_key='#'  # Permitir finalizar con #
    )
    
    # Instrucciones para el usuario
    if speech_result:
        gather.say(
            "¿Hay algo más en lo que pueda ayudarte? Presiona numeral para terminar.",
            language='es-ES',
            voice='alice'
        )
    else:
        # Primera vez, ya se hizo la pregunta en /voice
        gather.say(
            "Por favor, dime en qué puedo ayudarte.",
            language='es-ES',
            voice='alice'
        )
    
    response.append(gather)
    
    # Si no hay entrada después del timeout, finalizar la llamada
    response.say(
        "No recibí respuesta. Gracias por llamar. ¡Hasta luego!",
        language='es-ES',
        voice='alice'
    )
    response.hangup()
    
    return str(response)


@app.route('/status', methods=['POST'])
def status():
    """
    Maneja eventos de estado de la llamada
    """
    call_sid = request.form.get('CallSid')
    call_status = request.form.get('CallStatus')
    
    print(f"Llamada {call_sid} - Estado: {call_status}")
    
    # Limpiar conversación cuando termine la llamada
    if call_status in ['completed', 'failed', 'busy', 'no-answer']:
        if call_sid in conversations:
            del conversations[call_sid]
    
    return '', 200


if __name__ == '__main__':
    # Para desarrollo local, usar ngrok para exponer el servidor
    # ngrok http 5000
    # En producción (Heroku/Railway/Render), el puerto viene de la variable PORT
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
