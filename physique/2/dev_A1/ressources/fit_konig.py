import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Données expérimentales
frequencies = np.array([900, 1300, 1700, 2150, 2550, 3000, 3500, 4000, 4500, 5000])  # Fréquences (Hz)
lambdas = np.array([0.384, 0.270, 0.206, 0.162, 0.136, 0.114, 0.098, 0.086, 0.076, 0.068])  # Longueurs d'onde (m)

# Fonction pour le fit linéaire : v = λ * f
def linear_fit(x, a):
    return a * x

# Ajustement des données
popt, pcov = curve_fit(linear_fit, 1/frequencies, lambdas)
vitesse_son = popt[0]  # Coefficient a = vitesse du son (m/s)
incertitude = np.sqrt(np.diag(pcov))[0]  # Incertitude sur a

# Affichage des résultats
print(f"Vitesse du son mesurée : {vitesse_son:.3f} ± {incertitude:.3f} m/s")

# Tracé des données et du fit
plt.figure(figsize=(10, 6))
plt.scatter(1/frequencies, lambdas, color='red', label='Données expérimentales')
plt.plot(1/frequencies, linear_fit(1/frequencies, *popt), color='blue', label=f'Fit linéaire : $v = {vitesse_son:.3f} \, \text{{m/s}}$')

# Configuration du graphique
plt.title("Relation entre l'inverse de la fréquence et la longueur d'onde", fontsize=14)
plt.xlabel("$1/f$ (s)", fontsize=12)
plt.ylabel("$\lambda$ (m)", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Affichage
plt.savefig("konig.png")
