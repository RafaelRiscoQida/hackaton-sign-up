#!/bin/bash
# Script para iniciar el servidor Flask
# Asegúrate de tener el entorno virtual activado

echo "Iniciando servidor Flask en http://localhost:5000"
echo "Recuerda ejecutar ngrok en otra terminal: ngrok http 5000"
echo ""
python app.py
