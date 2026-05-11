import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# DONNÉES EXPÉRIMENTALES
# ============================================================
# Format : {tension: {"freq": [5, 10, 20], "CD": [...], "AB": [...], "coeff_nl": [...]}}
data = {
    "1V": {
        "freq": [5, 10, 20],
        "CD": [0.007, 0.011, 0.012],
        "AB": [0.022, 0.020, 0.015],
        "coeff_nl": [0.328, 0.519, 0.760]
    },
    "2V": {
        "freq": [5, 10, 20],
        "CD": [0.017, 0.021, 0.022],
        "AB": [0.046, 0.036, 0.028],
        "coeff_nl": [0.381, 0.571, 0.783]
    },
    "3V": {
        "freq": [5, 10, 20],
        "CD": [0.024, 0.029, 0.030],
        "AB": [0.056, 0.050, 0.039],
        "coeff_nl": [0.421, 0.587, 0.765]
    }
}

# ============================================================
# CRÉATION DES GRAPHIQUES
# ============================================================
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

# Couleurs pour chaque tension
colors = {'1V': 'blue', '2V': 'red', '3V': 'green'}
markers = {'1V': 'o', '2V': 's', '3V': '^'}

# Tracer CD(f)
for tension in data:
    ax1.plot(data[tension]["freq"], data[tension]["CD"],
             color=colors[tension],
             marker=markers[tension],
             label=f"{tension}",
             linewidth=2)
ax1.set_ylabel("CD (V)")
ax1.set_title("Écart maximal CD en fonction de la fréquence")
ax1.grid(True)
ax1.legend()

# Tracer AB(f)
for tension in data:
    ax2.plot(data[tension]["freq"], data[tension]["AB"],
             color=colors[tension],
             marker=markers[tension],
             label=f"{tension}",
             linewidth=2)
ax2.set_ylabel("AB (V)")
ax2.set_title("Déplacement total AB en fonction de la fréquence")
ax2.grid(True)
ax2.legend()

# Tracer coeff_nl(f)
for tension in data:
    ax3.plot(data[tension]["freq"], data[tension]["coeff_nl"],
             color=colors[tension],
             marker=markers[tension],
             label=f"{tension}",
             linewidth=2)
ax3.set_ylabel("Coefficient de non-linéarité")
ax3.set_title("Coefficient de non-linéarité en fonction de la fréquence")
ax3.set_xlabel("Fréquence (Hz)")
ax3.grid(True)
ax3.legend()

plt.tight_layout()
plt.savefig("foo.png")
