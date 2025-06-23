from scipy.integrate import solve_ivp

class ModeloTuberculosis:
    def __init__(self):
        self.params = {
            'u': 10, 'n': 0.01, 'b': 0.5, 'a1': 0.1, 'a2': 0.1,
            'c': 0.3, 'g': 0.05, 'h': 0.1, 'k': 0.6, 'gamma': 0.1,
            'r': 0.05, 'p': 0.7, 'd1': 0.005, 'd2': 0.01, 'm1': 0.5, 'm2': 0.3
        }
        self.Y0 = [710800, 8000, 217, 510, 768, 0]  # S, E, I, J, L, R

    def update_parameters(self, new_params):
        for key in self.params:
            if key in new_params:
                try:
                    self.params[key] = float(new_params[key])
                except ValueError:
                    pass

    def sistema(self, t, y):
        S, E, I, J, L, R = y
        p = self.params
        X = S + E + I + J + L + R
        beta = p['b'] * (1 - p['a1']) * ((1 - p['a2']) * I + p['m1'] * (1 - p['a2']) * J + p['m2'] * L) / X
        dS = p['u'] - (beta + p['n']) * S
        dE = p['c'] * beta * S - (p['n'] + p['g']) * E + (1 - p['p']) * p['r'] * L
        dI = (1 - p['c']) * beta * S + p['g'] * E - (p['n'] + p['d1'] + p['h']) * I
        dJ = p['k'] * p['h'] * I - (p['n'] + p['gamma']) * J
        dL = (1 - p['k']) * p['h'] * I - (p['n'] + p['d2'] + p['r']) * L
        dR = p['gamma'] * J + p['p'] * p['r'] * L - p['n'] * R
        return [dS, dE, dI, dJ, dL, dR]

    def simular(self, T=200, dt=1):
        t_eval = [i for i in range(0, T+1, dt)]
        sol = solve_ivp(self.sistema, [0, T], self.Y0, t_eval=t_eval, vectorized=False)
        return {
            't': sol.t.tolist(),
            'X_s': sol.y[0].tolist(),
            'X_e': sol.y[1].tolist(),
            'X_i': sol.y[2].tolist(),
            'X_j': sol.y[3].tolist(),
            'X_l': sol.y[4].tolist(),
            'X_r': sol.y[5].tolist()
        }