# Guía de Despliegue

## Opción 1: Railway (Recomendado - Gratis)

Railway es la opción más fácil y gratuita para desplegar tu aplicación.

### Pasos:

1. **Crear cuenta en Railway:**
   - Ve a https://railway.app
   - Regístrate con GitHub

2. **Crear nuevo proyecto:**
   - Click en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Conecta tu repositorio

3. **Configurar variables de entorno:**
   En Railway, ve a tu proyecto → Variables y agrega:
   ```
   TWILIO_ACCOUNT_SID=tu_account_sid
   TWILIO_AUTH_TOKEN=tu_auth_token
   TWILIO_PHONE_NUMBER=+1234567890
   TO_PHONE_NUMBER=+34602074744
   OPENAI_API_KEY=sk-tu-api-key
   ```

4. **Railway automáticamente:**
   - Detecta que es una app Python
   - Instala dependencias de `requirements.txt`
   - Ejecuta `Procfile`
   - Te da una URL pública (ej: `https://tu-app.railway.app`)

5. **Configurar WEBHOOK_URL:**
   - Copia la URL que Railway te da
   - Agrega en Railway Variables: `WEBHOOK_URL=https://tu-app.railway.app`
   - O úsala directamente en `make_call.py`

6. **Hacer llamada:**
   ```bash
   python make_call.py
   ```

---

## Opción 2: Render (Gratis)

Similar a Railway, también gratuito.

### Pasos:

1. **Crear cuenta en Render:**
   - Ve a https://render.com
   - Regístrate con GitHub

2. **Crear nuevo Web Service:**
   - Click en "New +" → "Web Service"
   - Conecta tu repositorio de GitHub
   - Configura:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app`

3. **Configurar variables de entorno:**
   En Render Dashboard → Environment:
   ```
   TWILIO_ACCOUNT_SID=tu_account_sid
   TWILIO_AUTH_TOKEN=tu_auth_token
   TWILIO_PHONE_NUMBER=+1234567890
   TO_PHONE_NUMBER=+34602074744
   OPENAI_API_KEY=sk-tu-api-key
   ```

4. **Obtener URL:**
   - Render te da una URL (ej: `https://tu-app.onrender.com`)
   - Agrega: `WEBHOOK_URL=https://tu-app.onrender.com`

5. **Hacer llamada:**
   ```bash
   python make_call.py
   ```

---

## Opción 3: Heroku

Heroku funciona bien pero ahora tiene costos. Si tienes créditos gratuitos, puedes usarlo.

### Pasos:

1. **Instalar Heroku CLI:**
   ```bash
   # Ubuntu/Debian
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login:**
   ```bash
   heroku login
   ```

3. **Crear app:**
   ```bash
   heroku create tu-app-name
   ```

4. **Configurar variables:**
   ```bash
   heroku config:set TWILIO_ACCOUNT_SID=tu_account_sid
   heroku config:set TWILIO_AUTH_TOKEN=tu_auth_token
   heroku config:set TWILIO_PHONE_NUMBER=+1234567890
   heroku config:set TO_PHONE_NUMBER=+34602074744
   heroku config:set OPENAI_API_KEY=sk-tu-api-key
   heroku config:set WEBHOOK_URL=https://tu-app-name.herokuapp.com
   ```

5. **Desplegar:**
   ```bash
   git push heroku main
   ```

6. **Hacer llamada:**
   ```bash
   python make_call.py
   ```

---

## Comparación

| Plataforma | Costo | Facilidad | Tiempo de Setup |
|------------|-------|-----------|-----------------|
| **Railway** | Gratis | ⭐⭐⭐⭐⭐ | 5 min |
| **Render** | Gratis | ⭐⭐⭐⭐ | 10 min |
| **Heroku** | De pago* | ⭐⭐⭐ | 15 min |
| **ngrok** | Gratis | ⭐⭐ | 2 min (pero requiere app local) |

*Heroku tiene un plan gratuito limitado

---

## Recomendación

**Usa Railway** - Es gratis, fácil y rápido. Una vez desplegado, tendrás una URL permanente que puedes usar en `WEBHOOK_URL`.

---

## Actualizar WEBHOOK_URL después del despliegue

Una vez que tengas la URL de tu app desplegada:

1. **Opción A: Actualizar en la plataforma (Recomendado)**
   - Agrega `WEBHOOK_URL` en las variables de entorno de Railway/Render/Heroku
   - La app la leerá automáticamente

2. **Opción B: Actualizar en .env local**
   ```env
   WEBHOOK_URL=https://tu-app.railway.app
   ```
   - Solo para cuando ejecutes `make_call.py` localmente
