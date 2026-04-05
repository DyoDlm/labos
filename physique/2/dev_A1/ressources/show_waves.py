import numpy as np
import matplotlib.pyplot as plt

# Paramètres des ondes
A = 1.0          # Amplitude
f = 1.0          # Fréquence (Hz)
omega = 2 * np.pi * f
phase_constructive = 0      # Déphasage pour interférence constructive (0 rad)
phase_destructive = np.pi   # Déphasage pour interférence destructive (π rad)

# Domaine temporel
t = np.linspace(0, 2, 1000)  # Temps de 0 à 2 secondes

# Ondes p1 et p2
p1 = A * np.sin(omega * t)

# Interférence constructive (p1 et p2 en phase)
p2_constructive = A * np.sin(omega * t + phase_constructive)
p_total_constructive = p1 + p2_constructive

# Interférence destructive (p1 et p2 en opposition de phase)
p2_destructive = A * np.sin(omega * t + phase_destructive)
p_total_destructive = p1 + p2_destructive

# Création des graphiques
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Graphique 1 : Interférence constructive
ax1.plot(t, p1, label='$p_1$', color='blue', linestyle='--')
ax1.plot(t, p2_constructive, label='$p_2$ (en phase)', color='green', linestyle='--')
ax1.plot(t, p_total_constructive, label='$p_1 + p_2$ (constructive)', color='red', linewidth=2)
ax1.set_title('Interférence constructive')
ax1.set_xlabel('Temps (s)')
ax1.set_ylabel('Amplitude')
ax1.legend()
ax1.grid(True)

# Graphique 2 : Interférence destructive
ax2.plot(t, p1, label='$p_1$', color='blue', linestyle='--')
ax2.plot(t, p2_destructive, label='$p_2$ (opposition de phase)', color='green', linestyle='--')
ax2.plot(t, p_total_destructive, label='$p_1 + p_2$ (destructive)', color='red', linewidth=2)
ax2.set_title('Interférence destructive')
ax2.set_xlabel('Temps (s)')
ax2.set_ylabel('Amplitude')
ax2.legend()
ax2.grid(True)

# Ajustement de l'espacement entre les graphiques
plt.tight_layout()

# Affichage
plt.savefig("ohwaw.png")
