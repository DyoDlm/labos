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

# Tracé de la réponse indicielle avec légende détaillée
plt.figure(figsize=(10, 5))
plt.plot(t, y, label=f'Réponse indicielle\nDépassement: {overshoot*100:.1f}%\nTemps de montée: {rise_time:.3f} s\nTemps d\'établissement: {settling_time:.3f} s')
plt.axhline(1, color='red', linestyle='--', label='Valeur finale')
plt.axvline(settling_time, color='green', linestyle=':', label=f'Temps d\'établissement: {settling_time:.3f} s')
plt.axvline(rise_time, color='orange', linestyle=':', label=f'Temps de montée: {rise_time:.3f} s')
plt.title("Réponse indicielle - Caractéristiques")
plt.xlabel("Temps [s]")
plt.ylabel("Amplitude")
plt.legend(loc='upper left')
plt.grid(True)
plt.savefig("__k2.png")

# Affichage des valeurs
print("\nCaractéristiques de la réponse indicielle :")
print(f"Dépassement maximal: {overshoot*100:.1f}%")
print(f"Temps de montée: {rise_time:.3f} s")
print(f"Temps d'établissement: {settling_time:.3f} s")
