import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Fonction de transfert en boucle fermée (à adapter)
G_cf = ctrl.TransferFunction([1.008], [1.2e-6, 0.00815, 1])

# Réponse indicielle
t, y = ctrl.step_response(G_cf)

# Calcul des caractéristiques
overshoot = np.max(y) - 1  # Dépassement en %
settling_time = np.where(np.abs(y - 1) < 0.05)[0][-1] * (t[1] - t[0])  # Temps d'établissement à 5%
rise_time = np.where(y >= 1)[0][0] * (t[1] - t[0])  # Temps de montée (0 à 100%)

# Tracé de la réponse indicielle avec annotations
plt.figure(figsize=(10, 5))
plt.plot(t, y, label='Réponse indicielle')
plt.axhline(1, color='red', linestyle='--', label='Valeur finale')
plt.axvline(settling_time, color='green', linestyle=':', label='Temps d\'établissement')
plt.axvline(rise_time, color='orange', linestyle=':', label='Temps de montée')
plt.title("Réponse indicielle - Caractéristiques")
plt.xlabel("Temps [s]")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)
plt.savefig("__k.png")

# Affichage des valeurs
print("\nTableau des caractéristiques :")
print("| Caractéristique | Valeur | Unité |")
print("|-----------------|--------|-------|")
print(f"| Dépassement maximal | {overshoot*100:.1f}% | % |")
print(f"| Temps de montée | {rise_time:.3f} | s |")
print(f"| Temps d'établissement | {settling_time:.3f} | s |")
