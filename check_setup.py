"""
Script para verificar que la configuración esté correcta
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 Verificando configuración...\n")

errors = []
warnings = []

# Verificar variables de entorno
required_vars = {
    'TWILIO_ACCOUNT_SID': 'Account SID de Twilio',
    'TWILIO_AUTH_TOKEN': 'Auth Token de Twilio',
    'TWILIO_PHONE_NUMBER': 'Número de teléfono de Twilio',
    'TO_PHONE_NUMBER': 'Número al que llamar',
    'OPENAI_API_KEY': 'API Key de OpenAI',
    'WEBHOOK_URL': 'URL del webhook (ngrok)'
}

for var, description in required_vars.items():
    value = os.getenv(var)
    if not value:
        errors.append(f"❌ {var} ({description}) - NO CONFIGURADO")
    elif 'your-' in value.lower() or 'example' in value.lower():
        warnings.append(f"⚠️  {var} - Parece ser un valor de ejemplo, verifica que sea correcto")
    else:
        # Ocultar valores sensibles
        if 'KEY' in var or 'TOKEN' in var or 'SID' in var:
            display_value = value[:10] + "..." if len(value) > 10 else "***"
        else:
            display_value = value
        print(f"✅ {var}: {display_value}")

# Verificar formato de números de teléfono
twilio_num = os.getenv('TWILIO_PHONE_NUMBER', '')
to_num = os.getenv('TO_PHONE_NUMBER', '')

if twilio_num and not twilio_num.startswith('+'):
    warnings.append("⚠️  TWILIO_PHONE_NUMBER debería empezar con + (ej: +1234567890)")

if to_num and not to_num.startswith('+'):
    warnings.append("⚠️  TO_PHONE_NUMBER debería empezar con + (ej: +34602074744)")

# Verificar formato de webhook
webhook_url = os.getenv('WEBHOOK_URL', '')
if webhook_url:
    if not webhook_url.startswith('http'):
        errors.append("❌ WEBHOOK_URL debe empezar con http:// o https://")
    elif 'ngrok' in webhook_url and not webhook_url.startswith('https'):
        warnings.append("⚠️  WEBHOOK_URL debería usar HTTPS con ngrok")

# Verificar API Key de OpenAI
openai_key = os.getenv('OPENAI_API_KEY', '')
if openai_key and not openai_key.startswith('sk-'):
    warnings.append("⚠️  OPENAI_API_KEY debería empezar con 'sk-'")

print("\n" + "="*50)

if errors:
    print("\n❌ ERRORES ENCONTRADOS:")
    for error in errors:
        print(f"  {error}")
    print("\nPor favor, corrige estos errores antes de continuar.")
else:
    print("\n✅ Todas las variables de entorno están configuradas")

if warnings:
    print("\n⚠️  ADVERTENCIAS:")
    for warning in warnings:
        print(f"  {warning}")

print("\n" + "="*50)
print("\n📋 Checklist para iniciar:")
print("  1. ✅ Variables de entorno configuradas")
print("  2. ⬜ Servidor Flask corriendo (python app.py)")
print("  3. ⬜ ngrok corriendo (ngrok http 5000)")
print("  4. ⬜ WEBHOOK_URL actualizado con la URL de ngrok")
print("  5. ⬜ Listo para hacer llamadas (python make_call.py)")
