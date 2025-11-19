import numpy as np
import matplotlib.pyplot as plt

# Données
x = np.array([0.01, 0.04, 0.09, 0.16, 0.25, 0.81])
y = np.array([0.0171, 0.0398, 0.0805, 0.1379, 0.2055, 0.6416])

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
equation = rf"$\lambda (I^2) = ({slope:.4f} \pm {slope_std:.4f}) I^2 + ({intercept:.4f} \pm {intercept_std:.4f})$"

# --- Tracé ---
plt.figure(figsize=(8,6))
plt.scatter(x, y, color='blue', label='Données')
plt.plot(x, y_pred, color='red', label=f'Regression linéaire\n{equation}')
plt.ylabel(r"$\lambda$ [$s^-1$]")
plt.xlabel(r"$I^2$ [A²]")
plt.legend(fontsize=10)
plt.grid(True)
#plt.show()
plt.savefig("lambda.png")
