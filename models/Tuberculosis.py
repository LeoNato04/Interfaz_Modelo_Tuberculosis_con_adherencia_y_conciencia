from scipy.integrate import solve_ivp

class ModeloTuberculosis:
    def __init__(self):
        self.params = {
            'u': 10300, 'n': 0.01, 'b': 0.5, 'a1': 0.1, 'a2': 0.1,
            'c': 0.3, 'g': 0.05, 'h': 0.1, 'k': 0.6, 'gamma': 0.1,
            'r': 0.05, 'p': 0.7, 'd1': 0.005, 'd2': 0.01, 'm1': 0.5, 'm2': 0.3
        }
        self.Y0 = [710800, 8000, 217, 510, 768, 0]  # S, E, I, J, T, R

    def update_parameters(self, new_params):
        for key in self.params:
            if key in new_params:
                try:
                    self.params[key] = float(new_params[key])
                except ValueError:
                    pass

    def sistema(self, t, y):
        S, E, I, J, T, R = y
        p = self.params
        X = S + E + I + J + T + R
        beta = p['b'] * (1 - p['a1']) * ((1 - p['a2']) * I + p['m1'] * (1 - p['a2']) * J + p['m2'] * T) / X

        dS = p['u'] - (beta + p['n']) * S
        dE = p['c'] * beta * S - (p['n'] + p['g']) * E + (1 - p['p']) * p['r'] * T
        dI = (1 - p['c']) * beta * S + p['g'] * E - (p['n'] + p['d1'] + p['h']) * I
        dJ = p['k'] * p['h'] * I - (p['n'] + p['gamma']) * J
        dT = (1 - p['k']) * p['h'] * I - (p['n'] + p['d2'] + p['r']) * T
        dR = p['gamma'] * J + p['p'] * p['r'] * T - p['n'] * R
        return [dS, dE, dI, dJ, dT, dR]

    def simular(self, T1=200, dt=1):
        t_eval = [i for i in range(0, T1+1, dt)]
        sol = solve_ivp(self.sistema, [0, T1], self.Y0, t_eval=t_eval, vectorized=False)
        return {
            'time': sol.t.tolist(),
            'S': sol.y[0].tolist(),
            'E': sol.y[1].tolist(),
            'I': sol.y[2].tolist(),
            'J': sol.y[3].tolist(),
            'T': sol.y[4].tolist(),
            'R': sol.y[5].tolist()
        }
        
    def calcular_beta_rb(self, ultimos_valores):
        p = self.params
        S, E, I, J, T, R = ultimos_valores
        X = S + E + I + J + T + R

        # z1 - z4 (corregido según el artículo)
        z1 = p['n'] + p['g']
        z2 = p['n'] + p['d1'] + p['h']
        z3 = p['n'] + p['gamma']
        z4 = p['n'] + p['d2'] + p['r']

        # beta efectivo
        beta = p['b'] * (1 - p['a1']) * ((1 - p['a2']) * I + p['m1'] * (1 - p['a2']) * J + p['m2'] * T) / X

        # Rb (según fórmula corregida del artículo)
        num = (1 - p['a1']) * p['b'] * (p['c'] * p['g'] + (1 - p['c']) * z1) * (
            (1 - p['a2']) * z4 * (z3 + p['m1'] * p['k'] * p['h']) + (1 - p['k']) * p['h'] * p['m2'] * z3
        )
        den = z3 * z1 * z2 * z4 - (1 - p['p']) * p['r'] * p['g'] * (1 - p['k']) * p['h']
        rb = num / den if den != 0 else float('nan')

        return beta, rb, z1, z2, z3, z4
