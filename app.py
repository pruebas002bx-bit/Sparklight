from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__, template_folder='templates')

# --- Almacenamiento en Memoria (SOLO PARA DEMO) ---
# Esta lista guardará las ubicaciones. Se reinicia si el servidor cae.
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
    """Recibe los datos de localización del frontend."""
    try:
        data = request.json
        
        if not data or 'latitude' not in data or 'longitude' not in data:
            return jsonify({'success': False, 'message': 'Datos incompletos'}), 400

        # 1. Obtener datos de localización
        location_data = {
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude')
        }

        # 2. Guardar la información
        submissions.append(location_data)
        print(f"Nueva ubicación recibida: {location_data}") # Para depuración

        return jsonify({'success': True, 'message': 'Ubicación recibida'}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'Error en el servidor'}), 500

# --- Ejecución ---
if __name__ == '__main__':
    # '0.0.0.0' es necesario para que OnRender pueda conectarse
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)