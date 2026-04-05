import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Fonction de transfert en boucle fermée (à adapter selon votre système)
G_cf = ctrl.TransferFunction([1.008], [1.2e-6, 0.00815, 1])

# Calcul des pôles en boucle fermée
poles = ctrl.poles(G_cf)
print("Pôles en boucle fermée :", poles)

# Tracé du lieu des pôles avec contrainte de dépassement
plt.figure(figsize=(8, 6))
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.scatter(np.real(poles), np.imag(poles), color='red', label='Pôles dominants')
plt.title("Lieu des pôles - Contrainte de dépassement de 5%")
plt.xlabel("Partie réelle")
plt.ylabel("Partie imaginaire")
plt.grid(True)
plt.legend()

# Ajout d'un cercle pour la contrainte de dépassement
theta = np.linspace(0, 2*np.pi, 100)
plt.plot(np.cos(theta), np.sin(theta), 'r--', label="Contrainte 5%")
plt.legend()

plt.savefig("__j.png")

# Tableau des pôles
print("\nTableau des pôles dominants :")
print("| Pôle | Partie réelle | Partie imaginaire |")
print("|------|---------------|--------------------|")
for i, pole in enumerate(poles):
    print(f"| Pole {i+1} | {np.real(pole):.3f} | {np.imag(pole):.3f} |")
