import numpy as np
import matplotlib.pyplot as plt

# Données expérimentales
V = np.array([5, 10, 15, 20])  # Tensions (V)
n = np.array([1, 2, 3, 4])     # Nombre de franges
d = n * 316.5                 # Déplacement (nm)

# Calcul de la pente (coefficient piézo-électrique)
k = np.polyfit(V, d, 1)[0]    # Pente de la droite d = k * V

# Tracer le graphique
plt.figure(figsize=(8, 6))
plt.plot(V, d, 'bo', label="Données expérimentales")
plt.plot(V, k * V, 'r--', label=f"Fit linéaire: d = {k:.1f} nm/V * V")
plt.xlabel("Tension (V)")
plt.ylabel("Déplacement (nm)")
plt.title("Déplacement du piézo en fonction de la tension")
plt.grid(True)
plt.legend()
plt.savefig("coeff.png")

print(f"Coefficient piézo-électrique : k = {k:.1f} nm/V")
