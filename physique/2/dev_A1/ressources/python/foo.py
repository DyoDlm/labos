import numpy as np




import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Constantes
g = 9.81
h = 0.008
rho = 990  # kg/m³

# Données expérimentales
lambda_exp = np.array([
    0.0119690744752372, 0.0105726824531262, 0.00957525958018974,
    0.00703183125420184, 0.00598453723761859, 0.00512960334653022,
    0.00448840292821394, 0.00418917606633301, 0.00374033577351162
])
v_exp = np.array([
    0.296, 0.318, 0.3344, 0.36425, 0.406, 0.425142857142857,
    0.45825, 0.4907, 0.495
])

# Fonction théorique complète (sans approximation)
def v_theorique(lambda_, gamma):
    return np.sqrt(
        (g * lambda_ / (2 * np.pi) + 2 * np.pi * gamma / (rho * lambda_))
        * np.tanh(2 * np.pi * h / lambda_)
    )

# Fonction pour le fit
def fit_function(lambda_, gamma):
    return v_theorique(lambda_, gamma)

# Ajustement
popt, pcov = curve_fit(fit_function, lambda_exp, v_exp, p0=[0.072])
gamma_opt = popt[0]

# Affichage des résultats
print(f"Tension superficielle ajustée : {gamma_opt:.4f} N/m")

# Vérification de l'approximation d'eau profonde
for l in lambda_exp:
    arg_tanh = 2 * np.pi * h / l
    print(f"Pour λ = {l:.6f} m, 2πh/λ = {arg_tanh:.3f} (tanh ≈ {np.tanh(arg_tanh):.3f})")

# Tracé
l_th = np.linspace(0.0038, 0.012, 400)
v_fit = v_theorique(l_th, gamma_opt)

plt.plot(l_th, v_fit, label=f"Fit expérimental (γ = {gamma_opt:.3f} N/m)")
plt.scatter(lambda_exp, v_exp, label="Valeurs expérimentales", color="red")
plt.xlim(0.003, 0.013)
plt.grid()
plt.xlabel(r"$\lambda$ [m]")
plt.ylabel(r"$c$ [m/s]")
plt.legend()
plt.savefig("fit_tension_superficielle.png")
#plt.show()
