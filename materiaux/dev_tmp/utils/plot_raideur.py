import numpy as np
import matplotlib.pyplot as plt

# Données
y = np.array([1,2,5,10,20])
x = np.array([140.5, 143.5, 148.6,150.5,155.7])

i = 0
for item in y:
    y[i] = np.log(item)
    i += 1

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
equation = rf"$M_f (\theta) = ({slope:.4f} \pm {slope_std:.4f}) \,\theta + ({intercept:.4f} \pm {intercept_std:.4f})$"
i = 0
for item in x:
    x[i] = 1/item
    i += 1

# --- Tracé ---
plt.figure(figsize=(8,6))
plt.scatter(x, y, color='blue', label='Données')
plt.plot(x, y_pred,color='red', label=f'Regression linéaire\n{equation}')
plt.ylabel(r"$M_f$ [Nm]")
plt.xlabel(r"$\theta$ [rad]")
plt.legend(fontsize=10)
plt.grid(True)
#plt.show()
plt.savefig("raideur.png")
