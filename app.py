from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "plusbus_secret_key_2026"

# Datos de viajes (simulados)
viajes_ejemplo = [
    {"id": 1, "empresa": "Trans Copacabana", "origen": "La Paz", "destino": "Cochabamba", 
     "fecha_salida": "2025-05-20", "hora_salida": "08:00", "duracion": "6h", 
     "precio": 80, "asientos_disponibles": 15, "imagen": "https://i.imgur.com/6b3qXJK.png"},
    {"id": 2, "empresa": "Flota Bolívar", "origen": "La Paz", "destino": "Santa Cruz", 
     "fecha_salida": "2025-05-20", "hora_salida": "14:30", "duracion": "12h", 
     "precio": 150, "asientos_disponibles": 8, "imagen": "https://i.imgur.com/6b3qXJK.png"},
    {"id": 3, "empresa": "Expreso Sucre", "origen": "Cochabamba", "destino": "Santa Cruz", 
     "fecha_salida": "2025-05-21", "hora_salida": "22:00", "duracion": "8h", 
     "precio": 100, "asientos_disponibles": 22, "imagen": "https://i.imgur.com/6b3qXJK.png"},
    {"id": 4, "empresa": "Transporte Potosí", "origen": "Potosí", "destino": "Sucre", 
     "fecha_salida": "2025-05-22", "hora_salida": "07:30", "duracion": "3h", 
     "precio": 45, "asientos_disponibles": 30, "imagen": "https://i.imgur.com/6b3qXJK.png"},
    {"id": 5, "empresa": "Andina Tours", "origen": "La Paz", "destino": "Tarija", 
     "fecha_salida": "2025-05-23", "hora_salida": "10:00", "duracion": "14h", 
     "precio": 180, "asientos_disponibles": 5, "imagen": "https://i.imgur.com/6b3qXJK.png"},
    {"id": 6, "empresa": "Oriente Bus", "origen": "Santa Cruz", "destino": "Trinidad", 
     "fecha_salida": "2025-05-24", "hora_salida": "09:00", "duracion": "7h", 
     "precio": 90, "asientos_disponibles": 12, "imagen": "https://i.imgur.com/6b3qXJK.png"},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pasajes')
def pasajes():
    return render_template('pasajes.html', viajes=viajes_ejemplo)

@app.route('/pago')
def pago():
    return render_template('pago.html')

@app.route('/turismo')
def turismo():
    return render_template('turismo.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    data = request.get_json()
    origen = data.get('origen', '')
    destino = data.get('destino', '')
    fecha = data.get('fecha', '')
    
    resultados = [v for v in viajes_ejemplo 
                  if (origen == '' or v['origen'].lower() == origen.lower())
                  and (destino == '' or v['destino'].lower() == destino.lower())
                  and (fecha == '' or v['fecha_salida'] == fecha)]
    
    resultados.sort(key=lambda x: x['hora_salida'])
    return jsonify(resultados)

@app.route('/buscar-global', methods=['POST'])
def buscar_global():
    query = request.get_json().get('query', '').lower()
    resultados = [v for v in viajes_ejemplo 
                  if query in v['origen'].lower() or 
                     query in v['destino'].lower() or
                     query in v['empresa'].lower()]
    return jsonify(resultados)

@app.route('/procesar-pago', methods=['POST'])
def procesar_pago():
    data = request.get_json()
    # Simular procesamiento exitoso
    return jsonify({"success": True, "mensaje": "Pago procesado correctamente. Ticket enviado a tu correo."})

if __name__ == '__main__':
    app.run(debug=True)