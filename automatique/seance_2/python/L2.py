import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Fonction de transfert du système complet
s = ctrl.TransferFunction.s
G_s = 1.008 / (1.2e-6 * s**2 + 0.00815 * s + 1)

# Gains du régulateur à tester
gains = [2500, 3306, 4500, 6000]
overshoots = []

plt.figure(figsize=(12, 6))
for k in gains:
    # Régulateur PI
    G_R = ctrl.TransferFunction([k * 8e-3, k], [1, 0])
    # Fonction de transfert en boucle fermée
    G_cf = ctrl.feedback(G_R * G_s, 1)
    # Réponse indicielle
    t, y = ctrl.step_response(G_cf)
    overshoot = np.max(y) - 1  # Dépassement en %
    overshoots.append(overshoot * 100)
    plt.plot(t, y, label=f"Gain k={k}, Dépassement={overshoot*100:.1f}%")

plt.title("Réponses indicielles pour différents gains du régulateur")
plt.xlabel("Temps [s]")
plt.ylabel("Amplitude")
plt.legend(loc='upper right')
plt.grid(True)
plt.xlim(0, 0.005)
plt.savefig("__l2.png")

# Tableau des résultats
print("\nTableau des gains et dépassements :")
print("| Dépassement souhaité | Gain du régulateur | Valeur de dépassement (%) |")
print("|----------------------|--------------------|-----------------------------|")
for i, k in enumerate(gains):
    print(f"| {'4.3%' if i==0 else '5.0%' if i==1 else '10%' if i==2 else '16.3%'} | {k} | {overshoots[i]:.1f}% |")
