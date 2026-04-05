import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Fonction de transfert en boucle fermée (à adapter)
G_cf = ctrl.TransferFunction([1.008], [1.2e-6, 0.00815, 1])

# Calcul des pôles en boucle fermée
poles = ctrl.poles(G_cf)

# Tracé du lieu des pôles avec légende détaillée
plt.figure(figsize=(8, 6))
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.scatter(np.real(poles), np.imag(poles), color='red', label=f'Pôles dominants: {poles}')

plt.title("Lieu des pôles - Contrainte de dépassement de 5%")
plt.xlabel("Partie réelle")
plt.ylabel("Partie imaginaire")
plt.grid(True)

# Ajout d'un cercle pour la contrainte de dépassement
theta = np.linspace(0, 2*np.pi, 100)
plt.plot(np.cos(theta), np.sin(theta), 'r--', label="Contrainte dépassement 5%")

plt.legend()
plt.savefig("__j2.png")

# Affichage des valeurs
print("\nPôles dominants :")
for i, pole in enumerate(poles):
    print(f"Pôle {i+1}: {pole:.3f}")
