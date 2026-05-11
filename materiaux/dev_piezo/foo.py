import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# --- Initialisation des données ---
# Tensions et fréquences
tensions = [1, 1, 1, 2, 2, 2, 3, 3, 3]
frequences = [5, 10, 20, 5, 10, 20, 5, 10, 20]

# Coordonnées des points A, B, C, D (x, y)
points_A = np.array([
    [1.074862, 0.01348918],
    [1.130558, 0.01563158],
    [1.218604, 0.01717277],
    [0.6477554, 0.0033509319999999996],
    [0.8404797, 0.005154575999999999],
    [0.9747612, 0.010983610000000001],
    [0.3982666, -0.003274636],
    [0.5720695, -0.001437422],
    [0.6218146, 0.004049806]
])

points_B = np.array([
    [1.951201, 0.035869929999999994],
    [1.898251, 0.03612171],
    [1.738792, 0.03237861],
    [2.330546, 0.048966949999999995],
    [2.217017, 0.04147618],
    [2.036653, 0.03909879],
    [2.862636, 0.05312357],
    [2.623219, 0.048820459999999996],
    [2.295755, 0.04261604]
])

points_C = np.array([
    [1.356548, 0.025296790000000003],
    [1.165197, 0.02352367],
    [0.9923093, 0.02085635],
    [0.5204931, 0.007339702],
    [0.5093539, 0.009512619000000002],
    [0.5035554, 0.016661580000000002],
    [1.627705, 0.038532670000000005],
    [-0.00091556, 0.004269539],
    [-0.00122074, 0.01149632]
])

points_D = np.array([
    [1.477096, 0.020480969999999998],
    [1.94525, 0.031969660000000004],
    [1.976684, 0.028238779999999998],
    [1.629841, 0.01899167],
    [1.727805, 0.01625111],
    [2.463607, 0.03236182],
    [1.816919, 0.01807916],
    [2.062288, 0.01761223],
    [2.307504, 0.01758629]
])

# Calcul de AB et CD (déplacements totaux et écarts maximaux)
AB = np.abs(points_B[:, 1] - points_A[:, 1])
CD = np.abs(points_C[:, 1] - points_D[:, 1])

# Coefficient de non-linéarité (C_N_L = CD / AB)
C_N_L = CD / AB

# --- Affichage des résultats ---
print("--- Données initialisées ---")
for i in range(len(tensions)):
    print(f"Tension: {tensions[i]} V, Fréquence: {frequences[i]} Hz")
    print(f"  A: {points_A[i]}, B: {points_B[i]}, C: {points_C[i]}, D: {points_D[i]}")
    print(f"  AB: {AB[i]:.6f} V, CD: {CD[i]:.6f} V, Coefficient de non-linéarité: {C_N_L[i]:.6f}")
    print("---")

# --- Traçage des courbes d'hystérésis ---
fig, axes = plt.subplots(3, 3, figsize=(15, 12))
axes = axes.ravel()  # Aplatir pour un accès facile

# Créer un dégradé de couleurs pour les labels
cmap = plt.cm.get_cmap('viridis', len(tensions))

for i in range(len(tensions)):
    ax = axes[i]
    U = tensions[i]
    f = frequences[i]

    # Extraire les points pour cette mesure
    A, B, C, D = points_A[i], points_B[i], points_C[i], points_D[i]

    # Tracer les points A, B, C, D
    ax.scatter([A[0], B[0], C[0], D[0]], [A[1], B[1], C[1], D[1]],
               color=['red', 'blue', 'green', 'purple'], label=f'U={U}V, f={f}Hz')

    # Tracer les lignes AB et CD
    ax.plot([A[0], B[0]], [A[1], B[1]], 'k--', label=f'AB = {AB[i]:.3f} V')
    ax.plot([C[0], D[0]], [C[1], D[1]], 'k:', label=f'CD = {CD[i]:.3f} V')

    # Ajouter un label avec le coefficient de non-linéarité
    ax.text(0.5, 0.9, f'Non-linéarité: {C_N_L[i]:.3f}',
            transform=ax.transAxes, ha='center', va='center',
            color=cmap(i), fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

    ax.set_xlabel('Temps (arbitraire)')
    ax.set_ylabel('Tension (V)')
    ax.set_title(f'U = {U} V, f = {f} Hz')
    ax.legend()
    ax.grid(True)

plt.tight_layout()
plt.savefig("foo.png")
