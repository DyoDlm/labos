import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Définition des fonctions de transfert
K_mot = 4.53e3
tau_mot = 8e-3
G_mot = ctrl.TransferFunction([K_mot], [tau_mot, 1])

K_ele = 20.8e-3
tau_ele = 1.5e-4
G_ele = ctrl.TransferFunction([K_ele], [tau_ele, 1])

K_mes = 10.7e-3
G_mes = ctrl.TransferFunction([K_mes], [1])

# Fonction de transfert complète
G_s = G_mot * G_ele * G_mes

# Régulateur PI
Tn = 8e-3

# Diagramme du lieu des pôles
plt.figure(figsize=(12, 6))
ctrl.root_locus(G_s, plot=True, grid=True)
plt.title("Lieu des pôles pour $G_s(s)$")
plt.xlabel("Partie réelle")
plt.ylabel("Partie imaginaire")

# Réponse indicielle pour différents gains
plt.figure(figsize=(12, 6))
for k in [0.1, 6, 1000]:
    G_R = ctrl.TransferFunction([k * Tn, k], [1, 0])
    G_cf = ctrl.feedback(G_R * G_s, 1)
    t, y = ctrl.step_response(G_cf)
    plt.plot(t, y, label=f"Gain k = {k}")

plt.title("Réponse indicielle pour différents gains du régulateur")
plt.xlabel("Temps [s]")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("LOOK.png")
