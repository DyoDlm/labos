import numpy as np
import matplotlib.pyplot as plt

# Données
y = np.array([0.006008, 0.009012,0.011265,0.013518,0.016522,0.021779,0.026285,0.027787,0.030040,0.033795])
x = np.array([0.522,0.773,0.970,1.143,1.276,1.847,2.171,2.297,2.470,2.772])

# --- Régression linéaire ---
n = len(x)
slope, intercept = np.polyfit(x, y, 1)

# Prédiction de y
y_pred = slope * x + intercept

# --- Calcul des incertitudes (formule comme Excel DROITEREG) ---
residuals = y - y_pred
residual_std = np.sqrt(np.sum(residuals**2) / (n - 2))  # écart-type des résidus

x_mean = np.mean(x)
Sxx = np.sum((x - x_mean)**2)

slope_std = residual_std / np.sqrt(Sxx)          # incertitude sur la pente
intercept_std = residual_std * np.sqrt(1/n + x_mean**2 / Sxx)  # incertitude sur l'ordonnée

# --- Equation avec incertitudes (LaTeX) ---
equation = rf"$M_f (\alpha) = ({slope:.4f} \pm {slope_std:.4f}) \,\alpha + ({intercept:.4f} \pm {intercept_std:.4f})$"

# --- Tracé ---
plt.figure(figsize=(8,6))
plt.scatter(x, y, color='blue', label='Données')
plt.plot(x, y_pred, color='red', label=f'Regression linéaire\n{equation}')
plt.ylabel(r"$M_f$ [Nm]")
plt.xlabel(r"$\alpha$ [rad]")
plt.legend(fontsize=10)
plt.grid(True)
#plt.show()
plt.savefig("raideur.png")
