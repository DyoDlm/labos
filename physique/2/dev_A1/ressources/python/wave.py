import numpy as np
import matplotlib.pyplot as plt

# Paramètres de l'onde
A = 1.0          # Amplitude
lambda_onde = 1.0  # Longueur d'onde (m)
f = 1.0          # Fréquence (Hz)
omega = 2 * np.pi * f  # Pulsation (rad/s)
k = 2 * np.pi / lambda_onde  # Nombre d'onde (rad/m)
phi = 0          # Phase initiale (rad)

# Domaine spatial (x) et temporel (t)
x = np.linspace(0, 3 * lambda_onde, 1000)  # Position (m)
t = 0  # Instant fixé pour visualiser l'onde dans l'espace

# Équation de l'onde indéformable : y(x,t) = A * sin(k*x - omega*t + phi)
y = A * np.sin(k * x - omega * t + phi)

# Création du graphique
fig, ax = plt.subplots(figsize=(12, 6))

# Tracé de l'onde
ax.plot(x, y, label=f'Onde : $y(x,t) = {A} \\cdot \\sin({k:.1f}x - \\omega t)$', color='blue', linewidth=2)

# Annotations des composantes
# 1. Amplitude
ax.axhline(A, color='gray', linestyle='--', alpha=0.5)
ax.axhline(-A, color='gray', linestyle='--', alpha=0.5)
ax.text(0.1, A + 0.1, f'Amplitude $A = {A}$', color='gray', fontsize=12)

# 2. Longueur d'onde (λ)
x_lambda = [lambda_onde, 2 * lambda_onde]
y_lambda = [0, 0]
ax.plot(x_lambda, y_lambda, color='red', linestyle='--', linewidth=1)
ax.text(lambda_onde / 2, -A - 0.2, f'Longueur d\'onde $\\lambda = {lambda_onde}$ m', color='red', fontsize=12, ha='center')

# 3. Période (T) et fréquence (f)
ax.text(2.5 * lambda_onde, A + 0.2, f'Période $T = 1/f = {1/f:.2f}$ s\nFréquence $f = {f}$ Hz', color='green', fontsize=12)

# 4. Phase (φ)
ax.text(0.5 * lambda_onde, 0.5 * A, f'Phase initiale $\\phi = {phi}$ rad', color='purple', fontsize=12)

# 5. Points clés pour une période
for i in range(3):
    x_period = i * lambda_onde
    ax.axvline(x_period, color='gray', linestyle=':', alpha=0.5)
    ax.text(x_period, -A - 0.3, f'{i}$\\lambda$', color='gray', fontsize=10, ha='center')

# Configuration du graphique
ax.set_title('Composantes d\'une onde indéformable', fontsize=16)
ax.set_xlabel('Position $x$ (m)', fontsize=14)
ax.set_ylabel('Amplitude $y(x,t)$', fontsize=14)
ax.set_xlim(0, 3 * lambda_onde)
ax.set_ylim(-1.5 * A, 1.5 * A)
ax.legend(fontsize=12)
ax.grid(True, linestyle='--', alpha=0.6)

# Affichage
plt.tight_layout()
plt.savefig("wave.png")
