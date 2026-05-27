import numpy as np
import matplotlib.pyplot as plt

# --- Données expérimentales ---
# Diode VERTICALE (Upp et Ueff)
alpha_vert = np.array([90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 12.5, 10, 7.5, 5, 2.5, 0, -2.5, -5, -7.5, -10, -12.5, -15, -17.5, -20, -22.5, -25, -27.5, -30, -35, -40, -45, -50, -55, -60])
Upp_vert = np.array([15, 12, 0, 10, 15, 14, 14, 22, 27, 37, 50, 55, 60, 65, 69, 75, 78, 80, 83, 86, 87, 87, 86, 83, 82, 80, 76, 72, 66, 60, 58, 54, 47, 44, 40, 29, 24, 16, 10, 6])
Ueff_vert = np.array([0, 0, 0, 4, 10, 8, 9, 14, 11, 17, 22, 30, 25, 34, 38, 38, 40, 43, 44, 45, 46, 47, 49, 43, 42, 41, 40, 35, 34, 33, 30, 29, 24, 23, 22, 18, 17, 12, 9, 6])

# Diode HORIZONTALE (Upp et Ueff)
alpha_horiz = np.array([90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 17.5, 15, 12.5, -20, -22.5, -25, -27.5, -30, -35, -40, -45, -50, -55, -60, -70, -75, -80])
Upp_horiz = np.array([1.2, 2, 3, 5.5, 8.7, 12, 15, 19, 21, 21, 20, 17, 14, 9.5, 7, 6, 4.5, 3.6, 8.5, 10, 11, 12, 13.5, 16, 19, 19, 20, 18, 15.7, 8, 4.7, 3])
Ueff_horiz = np.array([0.8, 1.4, 1.5, 3.2, 4.9, 6.7, 9, 10, 11, 11, 10, 9, 6.7, 4.8, 3.3, 2.7, 2, 1.8, 4, 4.5, 5.1, 6, 6.4, 7.5, 8.5, 9, 8.7, 8.5, 7.4, 3.9, 2.4, 1.2])

# --- Normalisation (diviser par le max) ---
def normaliser(data):
    return data / np.nanmax(data)

Upp_vert_norm  = normaliser(Upp_vert)
Ueff_vert_norm = normaliser(Ueff_vert)
Upp_horiz_norm  = normaliser(Upp_horiz)   # CORRIGÉ : était normaliser(Upp_vert)
Ueff_horiz_norm = normaliser(Ueff_horiz)

# --- Courbes théoriques (loi de Malus) ---
alpha_theo = np.linspace(-90, 90, 1000)
sin2_alpha = np.sin(np.radians(alpha_theo)) ** 2
cos2_alpha = np.cos(np.radians(alpha_theo)) ** 2

# --- Tracé ---
plt.figure(figsize=(12, 6))

# Diode VERTICALE
plt.subplot(1, 2, 1)
plt.scatter(alpha_vert, Upp_vert_norm, label="Upp (exp)", color='blue', s=20)
plt.scatter(alpha_vert, Ueff_vert_norm, label="Ueff (exp)", color='cyan', s=20)
plt.plot(alpha_theo, sin2_alpha, label=r"Loi de Malus: $I \propto \sin^2(\alpha)$", color='red', linestyle='--')
plt.title("Diode VERTICALE (parallèle à la polarisation)")
plt.xlabel("Angle α / °")
plt.ylabel("Intensité normalisée")
plt.ylim(0, 1.1)
plt.grid()
plt.legend()

# Diode HORIZONTALE
plt.subplot(1, 2, 2)
plt.scatter(alpha_horiz, Upp_horiz_norm, label="Upp (exp)", color='blue', s=20)
plt.scatter(alpha_horiz, Ueff_horiz_norm, label="Ueff (exp)", color='cyan', s=20)
plt.plot(alpha_theo, cos2_alpha, label=r"Loi de Malus: $I \propto \cos^2(\alpha)$", color='red', linestyle='--')
plt.title("Diode HORIZONTALE (perpendiculaire à la polarisation)")
plt.xlabel("Angle α / °")
plt.ylabel("Intensité normalisée")
plt.ylim(0, 1.1)
plt.grid()
plt.legend()

plt.tight_layout()
plt.savefig("loi_de_malus.png", dpi=300)
print("Saved loi_de_malus.png")
