import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


g = 9.81
h = 0.01
rho = 950  # kg/m³
SCALE_FACTOR = 1.67#facteur de correction

f = np.array([14.8,
18.0,
20.9,
31.0,
40.6,
49.6,
61.1,
70.1,
79.2])

lambda_exp = np.array([
    0.0119690744752372, 0.0105726824531262, 0.00957525958018974,
    0.00703183125420184, 0.00598453723761859, 0.00512960334653022,
    0.00448840292821394, 0.00418917606633301, 0.00374033577351162
])
D = np.array([40,53,48,47,60,60,45,49,50])
N = np.array([2,3,3,4,6,7,6,7,8])
lambda_exp = D / (N - 1)
lambda_exp *= 10**-3
print(f"Lanbda : {lambda_exp}")
lambda_exp /= SCALE_FACTOR


print(f"Lanbda : {lambda_exp}")

v_exp = np.array([
    0.296, 0.318, 0.3344, 0.36425, 0.406, 0.425142857142857,
    0.45825, 0.4907, 0.495
])

v_exp = lambda_exp * f
print(f"Vexp : {v_exp}")
def v_theorique(lambda_, gamma):
    return np.sqrt(
        (g * lambda_ / (2 * np.pi) + 2 * np.pi * gamma / (rho * lambda_))
        * np.tanh(2 * np.pi * h / lambda_)
    )

def fit_function(lambda_, gamma):
    return v_theorique(lambda_, gamma)

popt, pcov = curve_fit(fit_function, lambda_exp, v_exp, p0=[0.072])
gamma_opt = popt[0]

print(f"Tension superficielle ajustée : {gamma_opt:.4f} N/m")

l_th = np.linspace(min(lambda_exp) - min(lambda_exp)/10,
                   max(lambda_exp) + max(lambda_exp)/10, 
                   400)

v_fit = v_theorique(l_th, gamma_opt)

plt.plot(l_th, v_fit, label=f"Fit expérimental (γ = {gamma_opt:.3f} N/m)")
plt.scatter(lambda_exp, v_exp, label="Valeurs expérimentales", color="red")
#plt.xlim(0.003, 0.013)
plt.grid()
plt.xlabel(r"$\lambda$ [m]")
plt.ylabel(r"$c$ [m/s]")
plt.legend()
plt.savefig("fit_tension_superficielle.png")
#plt.show()
