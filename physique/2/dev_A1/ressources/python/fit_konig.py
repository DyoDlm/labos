import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

frequencies = np.array([900, 1300, 1700, 2150, 2550, 3000, 3500, 4000, 4500, 5000]) 
lambdas = np.array([0.384, 0.270, 0.206, 0.162, 0.136, 0.114, 0.098, 0.086, 0.076, 0.068])

def linear_fit(x, a):
    return a * x

popt, pcov = curve_fit(linear_fit, 1/frequencies, lambdas)
vitesse_son = popt[0]  
incertitude = np.sqrt(np.diag(pcov))[0]  # Incertitude sur a

print(f"Vitesse du son mesurée : {vitesse_son:.3f} ± {incertitude:.3f} m/s")

plt.figure(figsize=(10, 6))
plt.scatter(1/frequencies, lambdas, color='red', label='Données expérimentales')
plt.plot(1/frequencies, linear_fit(1/frequencies, *popt),
         color='blue',
         label=f'Fit linéaire : $\lambda (1/f) = ({vitesse_son:.2f} \pm {incertitude:.2f} [m/s] $')

plt.xlabel("$1/f$ \ s", fontsize=12)
plt.ylabel("$\lambda$ \ m", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Affichage
plt.savefig("konig.png")
