import numpy as np
import matplotlib.pyplot as plt

# --- Données expérimentales ---
# Diode VERTICALE
alpha_vert = np.array([90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 12.5, 10, 7.5, 5, 2.5, 0, -2.5, -5, -7.5, -10, -12.5, -15, -17.5, -20, -22.5, -25, -27.5, -30, -35, -40, -45, -50, -55, -60])
Ueff_vert = np.array([0, 0, 0, 4, 10, 8, 9, 14, 11, 17, 22, 30, 25, 34, 38, 38, 40, 43, 44, 45, 46, 47, 49, 43, 42, 41, 40, 35, 34, 33, 30, 29, 24, 23, 22, 18, 17, 12, 9, 6])

# Diode HORIZONTALE
alpha_horiz = np.array([90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 17.5, 15, 12.5, -20, -22.5, -25, -27.5, -30, -35, -40, -45, -50, -55, -60, -70, -75, -80])
Ueff_horiz = np.array([0.8, 1.4, 1.5, 3.2, 4.9, 6.7, 9, 10, 11, 11, 10, 9, 6.7, 4.8, 3.3, 2.7, 2, 1.8, 4, 4.5, 5.1, 6, 6.4, 7.5, 8.5, 9, 8.7, 8.5, 7.4, 3.9, 2.4, 1.2])

# --- Normalisation des données ---
E_eff_vert_norm = Ueff_vert / np.nanmax(Ueff_vert)
E_eff_horiz_norm = Ueff_horiz / np.nanmax(Ueff_horiz)

# --- Courbes théoriques (normalisées) ---
alpha_theo = np.linspace(-90, 90, 1000)
sin_alpha = np.abs(np.sin(np.radians(alpha_theo)))  # Diode verticale: E_eff ∝ sin(α)
cos_alpha = np.abs(np.cos(np.radians(alpha_theo)))  # Diode horizontale: E_eff ∝ cos(α)

# --- Tracé ---
plt.figure(figsize=(12, 6))

# Diode VERTICALE
plt.subplot(1, 2, 1)
plt.scatter(alpha_vert, E_eff_vert_norm, label="E_eff (exp)", color='blue', s=30)
plt.plot(alpha_theo, sin_alpha, label="Théorie: $E_{eff} \\propto |\\sin(\\alpha)|$", color='red', linestyle='--', linewidth=2)
plt.title("Diode VERTICALE : $E_{eff}(\\alpha)$")
plt.xlabel("Angle $\\alpha$ / °")
plt.ylabel("E_eff normalisé")
plt.ylim(0, 1.1)
plt.xlim(-90, 90)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

# Diode HORIZONTALE
plt.subplot(1, 2, 2)
plt.scatter(alpha_horiz, E_eff_horiz_norm, label="E_eff (exp)", color='green', s=30)
plt.plot(alpha_theo, cos_alpha, label="Théorie: $E_{eff} \\propto |\\cos(\\alpha)|$", color='red', linestyle='--', linewidth=2)
plt.title("Diode HORIZONTALE : $E_{eff}(\\alpha)$")
plt.xlabel("Angle $\\alpha$ / °")
plt.ylabel("E_eff normalisé")
plt.ylim(0, 1.1)
plt.xlim(-90, 90)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.tight_layout()
plt.savefig("E_eff_vs_alpha.png", dpi=300, bbox_inches='tight')
