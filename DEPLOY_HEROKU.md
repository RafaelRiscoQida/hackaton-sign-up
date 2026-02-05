# Guía de Despliegue en Heroku - Paso a Paso

## Pasos para Desplegar

### 1. Instalar Heroku CLI

```bash
# Ubuntu/Debian
curl https://cli-assets.heroku.com/install.sh | sh

# O con snap
snap install heroku --classic
```

### 2. Login en Heroku

```bash
heroku login
```

### 3. Inicializar Git (si no lo has hecho)

```bash
git init
git add .
git commit -m "Initial commit"
```

### 4. Crear la App en Heroku

```bash
heroku create tu-app-name
# O sin nombre (Heroku te dará uno aleatorio)
heroku create
```

**Importante:** Anota la URL que Heroku te da (ej: `https://tu-app-name.herokuapp.com`)

### 5. Configurar Variables de Entorno

```bash
heroku config:set TWILIO_ACCOUNT_SID=tu_account_sid_aqui
heroku config:set TWILIO_AUTH_TOKEN=tu_auth_token_aqui
heroku config:set TWILIO_PHONE_NUMBER=+18564926544
heroku config:set TO_PHONE_NUMBER=+34602074744
heroku config:set OPENAI_API_KEY=sk-tu-api-key-aqui
```

### 6. Configurar WEBHOOK_URL (DESPUÉS del despliegue)

Una vez que tengas la URL de tu app (ej: `https://tu-app-name.herokuapp.com`):

```bash
heroku config:set WEBHOOK_URL=https://tu-app-name.herokuapp.com
```

**Nota:** No necesitas agregar `/voice` al final, el código lo maneja automáticamente.

### 7. Desplegar

```bash
git push heroku main
# O si estás en otra rama:
git push heroku master
```

### 8. Verificar que está funcionando

```bash
# Ver logs
heroku logs --tail

# Verificar que la app responde
curl https://tu-app-name.herokuapp.com/voice
```

### 9. Hacer una Llamada

Desde tu máquina local (con `.env` configurado):

```bash
python make_call.py
```

O actualiza tu `.env` local con:
```env
WEBHOOK_URL=https://tu-app-name.herokuapp.com
```

## Verificar Variables de Entorno

```bash
# Ver todas las variables
heroku config

# Ver una específica
heroku config:get WEBHOOK_URL
```

## Actualizar Código

Cada vez que hagas cambios:

```bash
git add .
git commit -m "Descripción del cambio"
git push heroku main
```

## Ver Logs en Tiempo Real

```bash
heroku logs --tail
```

## Comandos Útiles

```bash
# Abrir la app en el navegador
heroku open

# Reiniciar la app
heroku restart

# Ver el estado
heroku ps

# Abrir una consola de Python en Heroku
heroku run python
```

## Troubleshooting

### Error: "No app specified"
```bash
# Especifica la app
heroku config --app tu-app-name
```

### Error: "Could not find Procfile"
Asegúrate de que `Procfile` esté en la raíz del proyecto y tenga:
```
web: gunicorn app:app
```

### La app no responde
```bash
# Verificar logs
heroku logs --tail

# Reiniciar
heroku restart
```

### Verificar que gunicorn está instalado
```bash
heroku run pip list | grep gunicorn
```
