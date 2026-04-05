import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Fonction de transfert du système complet (à adapter)
s = ctrl.TransferFunction.s
G_s = 1.008 / (1.2e-6 * s**2 + 0.00815 * s + 1)

# Calcul des marges de stabilité
gm, pm, wg, wp = ctrl.margin(G_s)

# Tracé du diagramme de Bode avec légende détaillée
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
ctrl.bode(G_s, dB=True, Hz=False, omega=np.logspace(-1, 3, 1000), margins=True)
plt.title("Diagramme de Bode - Marges de stabilité")
plt.legend(
    [
        "Gain (dB)",
        "Phase (deg)",
        f"Marge de phase: {pm:.1f}°",
        f"Marge de gain: {gm:.1f} dB"
    ],
    loc='upper right'
)

plt.tight_layout()
plt.savefig("__i2.png")

# Affichage des valeurs
print(f"Marge de phase : {pm:.1f}°")
print(f"Marge de gain : {gm:.1f} dB")
