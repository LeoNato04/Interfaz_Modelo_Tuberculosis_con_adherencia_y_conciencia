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
        modo = params.get('modo', 1)  # 1 por defecto

        modelo.update_parameters(params)
        T1 = params.get('days', 200)
        resultado = modelo.simular(T1=T1, dt=1)

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

        # Cálculo de beta efectivo
        X = sum(modelo.Y0)
        I, J, T = modelo.Y0[2], modelo.Y0[3], modelo.Y0[4]
        a1 = params.get('a1', 0.1)
        a2 = params.get('a2', 0.1)
        m1, m2 = modelo.params['m1'], modelo.params['m2']
        b = params.get('b', 0.5)
        beta = b * (1 - a1) * ((1 - a2) * I + m1 * (1 - a2) * J + m2 * T) / X

        # Cálculo de Rb según fórmula correcta del artículo
        n, c, g, h = modelo.params['n'], modelo.params['c'], modelo.params['g'], modelo.params['h']
        gamma, r = modelo.params['gamma'], modelo.params['r']
        p, k = modelo.params['p'], modelo.params['k']
        d1, d2 = modelo.params['d1'], modelo.params['d2']

        z1 = n + g
        z2 = n + d1 + h
        z3 = n + gamma
        z4 = n + d2 + r

        numerador = (1 - a1) * b * (c * g + (1 - c) * z1) * ((1 - a2) * z4 * (z3 + m1 * k * h) + (1 - k) * h * m2 * z3)
        denominador = z3 * z1 * z2 * z4 - (1 - p) * r * g * (1 - k) * h
        rb = numerador / denominador if denominador != 0 else 0

        return jsonify({
            'time': resultado['time'],
            'S': resultado['S'],
            'E': resultado['E'],
            'I': resultado['I'],
            'J': resultado['J'],
            'T': resultado['T'],
            'R': resultado['R'],
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
            },
            'beta_efectivo': beta,
            'rb': rb,
            'params_used': {
                'a1': a1,
                'a2': a2,
                'm1': m1,
                'm2': m2,
                'z1': z1,
                'z2': z2,
                'z3': z3,
                'z4': z4
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Nueva ruta para calcular resultados de las 6 EDOs en un tiempo específico
@app.route('/get_edo_results', methods=['POST'])
def get_edo_results():
    try:
        time = request.get_json().get('time')
        if not time or time < 0:
            return jsonify({'error': 'Tiempo inválido'}), 400

        # Simulación 1 (modo 1)
        modelo.update_parameters(modelo.params)
        resultado1 = modelo.simular(T1=time, dt=1)

        # Simulación 2 (modo 2: aplicamos cambio de parámetros)
        params2 = modelo.params.copy()
        params2['b'] *= 0.8
        params2['p'] = min(params2['p'] + 0.1, 1.0)
        modelo.update_parameters(params2)
        resultado2 = modelo.simular(T1=time, dt=1)

        return jsonify({
            'sim1': {
                'S': resultado1['S'][time],
                'E': resultado1['E'][time],
                'I': resultado1['I'][time],
                'J': resultado1['J'][time],
                'T': resultado1['T'][time],
                'R': resultado1['R'][time]
            },
            'sim2': {
                'S': resultado2['S'][time],
                'E': resultado2['E'][time],
                'I': resultado2['I'][time],
                'J': resultado2['J'][time],
                'T': resultado2['T'][time],
                'R': resultado2['R'][time]
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
