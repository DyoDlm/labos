import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Constantes
g = 9.81  # m/s²
h = 0.01  # Hauteur d'eau en m (1.5 cm)
rho = 997  # Densité de l'eau savonneuse en kg/m³
SCALE = 1.67
# Données expérimentales
f = np.array([14.8, 18.0, 20.9, 31.0, 40.6, 49.6, 61.1, 70.1, 79.2])
D = np.array([40, 53, 48, 47, 60, 60, 45, 49, 50])  # en mm
N = np.array([2, 3, 3, 4, 6, 7, 6, 7, 8])

# Conversion en mètres
D_m = D / 1000
lambda_exp = D_m / (N* SCALE)
#lambda_exp[5] += 0.001
#lambda_exp[6] += 0.001
#lambda_exp[7] += 0.001

# Calcul des vitesses expérimentales
v_exp = lambda_exp * f
print(lambda_exp)
print(v_exp)
def v_theorique(lambda_, gamma):
    return np.sqrt(
        (g * lambda_ / (2 * np.pi) + (2 * np.pi * gamma) / (rho * lambda_))
        * np.tanh((2 * np.pi * h) / lambda_)
    )

# Fonction de fit
def fit_function(lambda_, gamma):
    return v_theorique(lambda_, gamma)

# Fit des données
popt, pcov = curve_fit(fit_function, lambda_exp, v_exp, p0=[0.03], maxfev=10000)
gamma_opt = popt[0]

# Affichage de la tension superficielle ajustée
print(f"Tension superficielle ajustée : {gamma_opt:.4f} N/m")

# Tracer les données et le fit
l_th = np.linspace(min(lambda_exp) - min(lambda_exp)/10,
                   max(lambda_exp),# + max(lambda_exp)/10,
                   400)

v_fit = v_theorique(l_th, gamma_opt)

plt.scatter(lambda_exp, v_exp, label="Valeurs expérimentales", color="red")
plt.plot(l_th, v_fit, label=f"Fit théorique (γ = {gamma_opt:.4f} N/m)")
plt.grid()
plt.xlabel(r"$\lambda$ [m]")
plt.ylabel(r"$c$ [m/s]")
plt.legend()
plt.savefig("fit_tension_superficielle_eau_savonneuse.png")
