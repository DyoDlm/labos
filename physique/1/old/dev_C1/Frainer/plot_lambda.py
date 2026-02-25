import numpy as np
import matplotlib.pyplot as plt

# Données
x = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.9])
y = np.array([0.0171, 0.0398, 0.0805, 0.1379, 0.2055, 0.6416])

# --- Régression polynomiale du 2ème degré ---
coeffs = np.polyfit(x, y, 2)  # coeffs[0]*x^2 + coeffs[1]*x + coeffs[2]
a, b, c = coeffs

# --- Prédiction de y pour la courbe lisse ---
x_fit = np.linspace(min(x), max(x), 200)
y_fit = a*x_fit**2 + b*x_fit + c

# --- Tracé ---
plt.figure(figsize=(8,6))
plt.scatter(x, y, color='blue', label='Données')
plt.plot(x_fit, y_fit, color='red', label=f'Fit :\n$\lambda = {a:.4f}I^2 + {b:.4f}I + {c:.4f}$')
plt.xlabel(r"$I$ [A]")
plt.ylabel(r"$\lambda$ [$s^{-1}$]")
plt.grid(True)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig("lambda_quadratique.png")
plt.show()

