from flask import Flask, render_template, request, jsonify
from models.Tuberculosis import ModeloTuberculosis
import numpy as np

app = Flask(__name__)
modelo = ModeloTuberculosis()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_simulation', methods=['POST'])
def runSimulation():
    try:
        params = request.get_json()
        modelo.update_parameters(params)
        resultado = modelo.simular(T=200, dt=1)

        # Superficies Rb en base a combinaciones paramétricas ficticias
        a1_vals = np.linspace(0, 1, 10)
        a2_vals = np.linspace(0, 1, 10)
        gamma_vals = np.linspace(0.1, 0.9, 10)
        b_vals = np.linspace(0.1, 0.9, 10)
        p_vals = np.linspace(0, 1, 10)
        k_vals = np.linspace(0, 1, 10)
        g_vals = np.linspace(0, 1, 10)

        rb_a1_a2 = [[np.sin(i) + np.cos(j) for j in a2_vals] for i in a1_vals]
        rb_gamma_b = [[i * j for j in b_vals] for i in gamma_vals]
        rb_p_k = [[np.exp(-i) + j for j in k_vals] for i in p_vals]
        rb_g_k = [[np.log(i + 1) + j for j in k_vals] for i in g_vals]

        return jsonify({
            'time': resultado['t'],
            'S': resultado['X_s'],
            'E': resultado['X_e'],
            'I': resultado['X_i'],
            'J': resultado['X_j'],
            'L': resultado['X_l'],
            'R': resultado['X_r'],
            'rb_surfaces': {
                'a1': list(a1_vals),
                'a2': list(a2_vals),
                'gamma': list(gamma_vals),
                'b': list(b_vals),
                'p': list(p_vals),
                'k': list(k_vals),
                'g': list(g_vals),
                'rb_a1_a2': rb_a1_a2,
                'rb_gamma_b': rb_gamma_b,
                'rb_p_k': rb_p_k,
                'rb_g_k': rb_g_k
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Nueva ruta para calcular resultados de las 6 EDOs en un tiempo específico
@app.route('/get_edo_results', methods=['POST'])
def get_edo_results():
    try:
        # Recibe el tiempo en días
        time = request.get_json().get('time')
        if not time or time < 0:
            return jsonify({'error': 'Tiempo inválido'}), 400

        # Asumiendo que ya tienes una función en ModeloTuberculosis para resolver las EDOs
        # Aquí llamamos al modelo y obtenemos los resultados para el tiempo específico
        resultado = modelo.simular(T=time, dt=1)

        # Los resultados se formatean para enviar al frontend
        edo_results = {
            'S': resultado['X_s'][time],  # Susceptibles
            'E': resultado['X_e'][time],  # Latentes
            'I': resultado['X_i'][time],  # Infectados no diagnosticados
            'J': resultado['X_j'][time],  # Infectados con conciencia
            'L': resultado['X_l'][time],  # Infectados sin conciencia
            'R': resultado['X_r'][time],  # Recuperados
        }

        return jsonify(edo_results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)