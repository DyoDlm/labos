import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Constantes
g = 9.81
h = 0.01
rho = 950  # kg/m³

# Données
f = np.array([14.8, 18.0, 20.9, 31.0, 40.6, 49.6, 61.1, 70.1, 79.2])
D = np.array([40, 53, 48, 47, 60, 60, 45, 49, 50])
N = np.array([2, 3, 3, 4, 6, 7, 6, 7, 8])

# Calcul des longueurs d'onde avec les deux méthodes
lambda_exp_N = D / N * 10**-3
lambda_exp_N_minus_1 = D / (N - 1) * 10**-3

# Calcul des vitesses expérimentales
v_exp_N = lambda_exp_N * f
v_exp_N_minus_1 = lambda_exp_N_minus_1 * f

# Fonction théorique de la vitesse de phase
def v_theorique(lambda_, gamma):
    return np.sqrt(
        (g * lambda_ / (2 * np.pi) + 2 * np.pi * gamma / (rho * lambda_))
        * np.tanh(2 * np.pi * h / lambda_)
    )

# Fonction de fit
def fit_function(lambda_, gamma):
    return v_theorique(lambda_, gamma)

# Fit des données avec les deux méthodes
popt_N, pcov_N = curve_fit(fit_function, lambda_exp_N, v_exp_N, p0=[0.072], maxfev=10000)
gamma_opt_N = popt_N[0]

popt_N_minus_1, pcov_N_minus_1 = curve_fit(fit_function, lambda_exp_N_minus_1, v_exp_N_minus_1, p0=[0.072], maxfev=10000)
gamma_opt_N_minus_1 = popt_N_minus_1[0]

# Affichage des tensions superficielles ajustées
print(f"Tension superficielle ajustée (N) : {gamma_opt_N:.4f} N/m")
print(f"Tension superficielle ajustée (N-1) : {gamma_opt_N_minus_1:.4f} N/m")

# Tracer les données et les fits
l_th = np.linspace(min(lambda_exp_N_minus_1) - min(lambda_exp_N_minus_1)/10,
                   max(lambda_exp_N_minus_1) + max(lambda_exp_N_minus_1)/10,
                   400)

v_fit_N = v_theorique(l_th, gamma_opt_N)
v_fit_N_minus_1 = v_theorique(l_th, gamma_opt_N_minus_1)

plt.plot(l_th, v_fit_N, label=f"Fit théorique (γ = {gamma_opt_N:.3f} N/m) avec N")
plt.plot(l_th, v_fit_N_minus_1, label=f"Fit théorique (γ = {gamma_opt_N_minus_1:.3f} N/m) avec N-1", linestyle='--')
plt.scatter(lambda_exp_N, v_exp_N, label="Valeurs expérimentales avec N", color="red")
plt.scatter(lambda_exp_N_minus_1, v_exp_N_minus_1, label="Valeurs expérimentales avec N-1", color="blue")
plt.grid()
plt.xlabel(r"$\lambda$ [m]")
plt.ylabel(r"$c$ [m/s]")
plt.legend()
plt.savefig("ll.png")
