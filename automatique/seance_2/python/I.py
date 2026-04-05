import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Fonction de transfert du système complet (à adapter selon votre système)
s = ctrl.TransferFunction.s
G_s = 1.008 / (1.2e-6 * s**2 + 0.00815 * s + 1)

# Calcul des marges de stabilité
gm, pm, wg, wp = ctrl.margin(G_s)

# Tracé du diagramme de Bode avec annotations
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
ctrl.bode(G_s, dB=True, Hz=False, omega=np.logspace(-1, 3, 1000), margins=True)
plt.title("Diagramme de Bode - Marges de stabilité")
plt.gcf().text(0.5, 0.01, f"Marge de phase : {pm:.1f}°\nMarge de gain : {gm:.1f} dB", ha='center')

plt.tight_layout()
plt.savefig("__i.png")

# Affichage des valeurs
print(f"Marge de phase : {pm:.1f}°")
print(f"Marge de gain : {gm:.1f} dB")
