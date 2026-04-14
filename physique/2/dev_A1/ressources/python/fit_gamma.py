import numpy as np

import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

g = 9.81
h = 0.01
rho = 990

def v_theorique(lambda_, gamma):
    #lambda_ /= 2
    #return np.sqrt((g * lambda_ / (2 * np.pi) + gamma * 2 * np.pi / (rho * lambda_)) * np.tanh(2 * np.pi * h / lambda_))
    return np.sqrt(
        (g * lambda_ / (2 * np.pi) + 2 * np.pi * gamma / (rho * lambda_))
        * np.tanh(2 * np.pi * h / lambda_)
        )

lambda_exp = np.array([0.0119690744752372,
0.0105726824531262,
0.00957525958018974,
0.00703183125420184,
0.00598453723761859,
0.00512960334653022,
0.00448840292821394,
0.00418917606633301,
0.00374033577351162
])

lambda_2 = np.array([0.005, # grossissement 4
0.00441666666666667,
0.004,
0.0029375,
0.0025,
0.00214285714285714,
0.001875,
0.00175,
0.0015625
])

v_exp = np.array([0.296,
0.318,
0.3344,
0.36425,
0.406,
0.425142857142857,
0.45825,
0.4907,
0.495
])
lambda_initial = np.array([0.0400, 0.0265, 0.0240, 0.0157, 0.0120, 0.0100, 0.0090, 0.0083, 0.0071])

v_exp = np.array([0.592, 0.477, 0.5016, 0.485666666666667, 0.4872, 0.496, 0.5499, 0.572483333333333, 0.565714285714286])
lambda_exp = np.array([0.04, 0.0265, 0.024, 0.0156666666666667, 0.012, 0.01, 0.009, 0.00816666666666667, 0.00714285714285714])

def fit_function(lambda_, gamma):
    return v_theorique(lambda_, gamma)

popt, pcov = curve_fit(fit_function, lambda_exp, v_exp, p0=[0.072])

l_th = np.linspace(min(lambda_exp), max(lambda_exp) + 0.001, 400)

v_th = v_theorique(l_th, 0.072)

v_fit = v_theorique(l_th, popt)

plt.plot(l_th, v_fit, label="Fit experimental")
#plt.scatter(l_th, v_th, label="Valeurs theoriques")
#plt.xlim(0.003, 0.013)
#plt.scatter(lambda_2, v_exp, label="Valeurs experimentales (x4)")
plt.scatter(lambda_exp, v_exp, color='r', label="Valeurs experimentales (x1,67)")
plt.grid()
plt.xlabel(rf"$ \lambda $" + " \ m")
plt.ylabel("c \ m/s")
plt.legend()
plt.savefig("foo.png")
print(popt, pcov)

# Résultat
gamma_opt = popt[0]
print(f"La tension superficielle ajustée est : {gamma_opt:.4f} N/m")

