import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Données expérimentales (à adapter avec vos valeurs)
# Format : [Tension (V), Fréquence (Hz), Pente (nm/V)]
data = np.array([
    # 1 V
    [1, 5, 0.328],
    [1, 10, 0.519],
    [1, 20, 0.760],

    # 2 V
    [2, 5, 0.381],
    [2, 10, 0.571],
    [2, 20, 0.783],

    # 3 V
    [3, 5, 0.421],
    [3, 10, 0.587],
    [3, 20, 0.765]
])

# Extraire les fréquences et les pentes
frequences = data[:, 1]  # Fréquences (Hz)
pentes = data[:, 2]     # Pentes (nm/V)
tensions = data[:, 0]   # Tensions (V)

# Fonction pour le fit linéaire : y = a * x + b
def linear_fit(x, a, b):
    return a * x + b

# Effectuer le fit linéaire sur l'ensemble des points
popt, pcov = curve_fit(linear_fit, frequences, pentes)
a_fit, b_fit = popt  # Coefficients du fit : a (pente), b (ordonnée à l'origine)
print(f"Fit linéaire : y = {a_fit:.4f} * x + {b_fit:.4f}")

# Initialisation du graphique
plt.figure(figsize=(10, 6))
plt.title("Évolution du coefficient de non-linéarité en fonction de la frequence", fontsize=14)
plt.xlabel("Fréquence (Hz)", fontsize=12)
plt.ylabel("Pente $d_{33}$ (nm/V)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Couleurs pour chaque tension
colors = ['green', 'blue', 'red']
labels = [f"{V} V" for V in np.unique(tensions)]

# Tracer une courbe par tension
for i, V in enumerate(np.unique(tensions)):
    mask = tensions == V
    x = frequences[mask]
    y = pentes[mask]
    plt.scatter(x, y, marker='o', linestyle='-', color=colors[i], label=labels[i])

# Tracer le fit linéaire sur l'ensemble des points
x_fit = np.linspace(min(frequences), max(frequences), 100)
y_fit = linear_fit(x_fit, *popt)
plt.plot(x_fit, y_fit, linestyle='--', color='black', linewidth=2, label=f"Fit linéaire: CNL(f) = {a_fit:.2f}f + {b_fit:.2f}")

# Ajouter une légende
plt.legend(title="Tension appliquée", fontsize=10)

# Sauvegarder le graphique
plt.savefig("pentes.png", dpi=300, bbox_inches='tight')
