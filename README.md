# Twilio + Agente de IA Conversacional

Sistema que integra Twilio con un agente de IA para mantener conversaciones de voz bidireccionales.

## Características

- ✅ Reconocimiento de voz en tiempo real
- ✅ Integración con OpenAI GPT para respuestas inteligentes
- ✅ Conversación bidireccional natural
- ✅ Mantenimiento de contexto durante la llamada
- ✅ Soporte para español

## Requisitos

- Python 3.8+
- Cuenta de Twilio con número de teléfono
- API Key de OpenAI
- **Despliegue en la nube** (Railway/Render/Heroku) **o ngrok** para desarrollo local

> 💡 **Recomendación:** Usa Railway (gratis) para tener una URL permanente. Ver [DEPLOY.md](DEPLOY.md) para instrucciones detalladas.

## Instalación

1. **Crear entorno virtual:**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

## Configuración

### 1. Variables de Entorno (.env)

```env
TWILIO_ACCOUNT_SID=tu_account_sid
TWILIO_AUTH_TOKEN=tu_auth_token
TWILIO_PHONE_NUMBER=+1234567890
TO_PHONE_NUMBER=+34602074744
OPENAI_API_KEY=sk-tu-api-key
WEBHOOK_URL=http://tu-ngrok-url.ngrok.io
```

### 2. Exponer el servidor localmente con ngrok

Para desarrollo, necesitas exponer tu servidor local usando ngrok:

```bash
# 1. Instalar ngrok (si no lo tienes)
# Descargar desde: https://ngrok.com/download
# O con snap: snap install ngrok

# 2. Ejecutar ngrok en una terminal
ngrok http 5000

# 3. Copiar la URL HTTPS que ngrok muestra (ej: https://abc123.ngrok.io)
# 4. Actualizar WEBHOOK_URL en .env con esa URL
# Ejemplo: WEBHOOK_URL=https://abc123.ngrok.io
```

**Importante:** 
- Usa la URL **HTTPS** (no HTTP) que ngrok proporciona
- La URL cambia cada vez que reinicias ngrok (a menos que tengas cuenta de pago)
- Mantén ngrok corriendo mientras uses el servidor

### 3. Configurar webhook en Twilio (opcional)

Si tienes un dominio, puedes configurar el webhook directamente en la consola de Twilio.

## Uso

### Opción 1: Sin ngrok (Solo mensajes, sin conversación bidireccional)

**Ventaja:** No necesitas exponer tu servidor, todo funciona localmente.

**Limitación:** Solo puedes enviar mensajes, no capturar respuestas del usuario.

```bash
python make_call_ai_local.py
```

Este script genera un mensaje con IA y lo envía, pero no puede escuchar la respuesta del usuario.

### Opción 2: Desplegado en la nube (Recomendado - Conversación bidireccional completa)

**Ventaja:** Conversación completa + URL permanente + No necesitas mantener tu PC encendida.

**Plataformas:** Railway (gratis), Render (gratis), o Heroku.

**Ver:** [DEPLOY.md](DEPLOY.md) para instrucciones detalladas de despliegue.

### Opción 3: Con ngrok (Solo para desarrollo local)

**Ventaja:** Conversación completa donde el usuario puede hablar y el agente responde.

**Requisito:** Necesitas exponer tu servidor con ngrok (solo para desarrollo).

#### 1. Iniciar el servidor Flask

En una terminal:
```bash
python app.py
# O usar el script: ./start.sh
```

El servidor estará disponible en `http://localhost:5000`

#### 2. Exponer con ngrok (en OTRA terminal)

```bash
ngrok http 5000
```

Verás algo como:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:5000
```

**Copiar la URL HTTPS** (ej: `https://abc123.ngrok.io`) y actualizar `WEBHOOK_URL` en `.env`:
```env
WEBHOOK_URL=https://abc123.ngrok.io
```

#### 3. Iniciar una llamada

En otra terminal (o la misma donde está Flask):
```bash
python make_call.py
```

**Flujo completo:**
1. Terminal 1: `python app.py` (servidor Flask)
2. Terminal 2: `ngrok http 5000` (túnel público)
3. Actualizar `.env` con la URL de ngrok
4. Terminal 3: `python make_call.py` (iniciar llamada)

## ¿Por qué necesito ngrok?

**Para conversación bidireccional:** Cuando el usuario habla, Twilio necesita enviar el audio transcrito a tu servidor para que la IA pueda procesarlo y responder. Esto requiere que tu servidor sea accesible desde internet (por eso ngrok o un servidor en la nube).

**Sin ngrok:** Solo puedes enviar mensajes predefinidos, pero no puedes capturar lo que dice el usuario en tiempo real.

## Endpoints

- `POST /voice` - Endpoint inicial cuando se recibe una llamada
- `POST /gather` - Procesa la entrada de voz y genera respuesta de IA
- `POST /status` - Maneja eventos de estado de la llamada

## Flujo de Conversación

1. Usuario recibe/realiza llamada
2. Twilio llama a `/voice` → Saludo inicial
3. Twilio redirige a `/gather` → Captura voz del usuario
4. Se transcribe el audio a texto
5. Se envía texto a OpenAI GPT
6. Se genera respuesta de IA
7. Se convierte respuesta a voz (TTS)
8. Se reproduce respuesta y se vuelve a capturar voz
9. Repetir desde paso 3 hasta que termine la llamada

## Personalización

### Cambiar el idioma

En `app.py`, cambiar los parámetros `language`:
- `'es-ES'` - Español (España)
- `'es-MX'` - Español (México)
- `'en-US'` - Inglés

### Cambiar el modelo de IA

En `app.py`, función `get_ai_response()`:
```python
response = openai.ChatCompletion.create(
    model="gpt-4",  # Cambiar a gpt-4 si tienes acceso
    ...
)
```

### Personalizar el prompt del sistema

En `app.py`, función `get_ai_response()`:
```python
messages = [
    {
        "role": "system",
        "content": "Tu prompt personalizado aquí"
    }
]
```

## Producción

Para producción, considera:

- Usar Redis o base de datos para almacenar conversaciones
- Implementar autenticación para webhooks
- Usar un servidor WSGI como Gunicorn
- Configurar HTTPS
- Implementar logging y monitoreo
- Manejar errores y timeouts

## Solución de Problemas

### Error: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Error: "OpenAI API key not found"
Verificar que `OPENAI_API_KEY` esté en el archivo `.env`

### La llamada no funciona
- Verificar que ngrok esté corriendo
- Verificar que la URL en `.env` sea correcta
- Verificar logs del servidor Flask

## Licencia

MIT
