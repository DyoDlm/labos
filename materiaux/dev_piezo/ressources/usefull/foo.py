import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# GROUPES DE FICHIERS
# ============================================================
groups = {
    "1V": ["1V5Hz_15.csv", "1V10Hz_15.csv", "1V20Hz_15.csv"],
    "2V": ["2V5Hz_15.csv", "2V10Hz_15.csv", "2V20Hz_15.csv"],
    "3V": ["3V5Hz_15.csv", "3V10Hz_15.csv", "3V20Hz_15.csv"]
}

i = 0

import numpy as np
import matplotlib.pyplot as plt

def ecart_CD(canal_A, canal_B, ax=None, color_C='blue', color_D='cyan', marker_size=100, label_C="C", label_D="D"):
    """
    Calcule les points C et D comme les points d'écart maximal entre les branches montante et descendante.
    Trace les points sur la courbe d'hystérésis si un axe est fourni.

    Args:
        canal_A (array): Tableau des tensions (V).
        canal_B (array): Tableau des déplacements (V ou µm).
        ax (matplotlib.axes): Axe pour tracer C et D.
        color_C, color_D (str): Couleurs des points C et D.
        marker_size (int): Taille des marqueurs.
        label_C, label_D (str): Légendes pour C et D.

    Returns:
        tuple: (C, D) où C et D sont des tuples (tension, déplacement).
    """
    canal_A_array = np.array(canal_A)
    canal_B_array = np.array(canal_B)

    # 1. Séparer les branches montante et descendante
    # Calculer la dérivée de la tension pour identifier les branches
    dA = np.gradient(canal_A_array)
    rising_indices = np.where(dA > 0)[0]  # Branche montante (dA > 0)
    falling_indices = np.where(dA < 0)[0]  # Branche descendante (dA < 0)

    # 2. Pour chaque tension, trouver les déplacements min/max entre les branches
    unique_V = np.unique(canal_A_array)
    max_deviations = []

    for V in unique_V:
        # Trouver les déplacements pour cette tension dans les deux branches
        rising_B = canal_B_array[(canal_A_array == V) & (np.isin(np.arange(len(canal_A_array)), rising_indices))]
        falling_B = canal_B_array[(canal_A_array == V) & (np.isin(np.arange(len(canal_A_array)), falling_indices))]

        if len(rising_B) > 0 and len(falling_B) > 0:
            # Écart entre les branches à cette tension
            deviation = np.max(rising_B) - np.min(falling_B)
            max_deviations.append((V, deviation, np.max(rising_B), np.min(falling_B)))

    if not max_deviations:
        # Cas dégénéré : pas de branches montante/descendante claires
        C = (np.nan, np.nan)
        D = (np.nan, np.nan)
    else:
        # 3. Trouver la tension avec l'écart maximal
        max_deviations = np.array(max_deviations)
        idx_max = np.argmax(max_deviations[:, 1])
        V_max, CD, B_rising, B_falling = max_deviations[idx_max]

        # Points C (branche montante) et D (branche descendante) à V_max
        C = (V_max, B_rising)
        D = (V_max, B_falling)

    # 4. Tracer C et D si un axe est fourni
    if ax is not None and not np.isnan(C[0]):
        ax.scatter([C[0]], [C[1]], color=color_C, s=marker_size, zorder=5, label=label_C)
        ax.scatter([D[0]], [D[1]], color=color_D, s=marker_size, zorder=5, label=label_D)
        ax.legend()

    return C, D

# ============================================================
for tension, files in groups.items():
    # Créer une figure pour cette tension
    fig_hys, ax_hys = plt.subplots(figsize=(8, 6))

    for file in files:
        # Lecture CSV
        df = pd.read_csv(file, skiprows=2)
        canal_A = df.iloc[:, 1].values
        canal_B = df.iloc[:, 2].values / 1000  # mV -> V

        # Extraction fréquence
        if "5Hz" in file:
            freq = "5 Hz"
        elif "10Hz" in file:
            freq = "10 Hz"
        elif "20Hz" in file:
            freq = "20 Hz"
        else:
            freq = "?"

        # Tracer la courbe d'hystérésis
        ax_hys.plot(canal_A, canal_B, linewidth=1.5, label=freq)

        # Appeler la fonction ecart_CD pour cette fréquence
        C, D = ecart_CD(
            canal_A,
            canal_B,
            ax=ax_hys,
            color_C='blue',
            color_D='cyan',
            marker_size=100,
            label_C=f"C ({freq})",
            label_D=f"D ({freq})"
        )
        if not np.isnan(C[0]):
            ax_hys.plot([C[0], D[0]], [C[1], D[1]], 'k-', linewidth=1, linestyle='--', alpha=0.7)

        
        # Afficher les résultats pour cette fréquence
        AB = np.max(canal_B) - np.min(canal_B)
        CD = np.abs(C[1] - D[1])
        non_linearity = CD / AB if AB != 0 else 0

        print(f"\nFichier: {file}")
        print(f"Points: A={np.min(canal_B):.3f}, B={np.max(canal_B):.3f}")
        print(f"C={C}, D={D}")
        print(f"AB={AB:.3f} V, CD={CD:.3f} V, Non-linéarité={non_linearity:.3f}")

    # Finaliser la figure
    ax_hys.set_xlabel("Tension (V)")
    ax_hys.set_ylabel("Déplacement (V)")
    ax_hys.set_title(f"Boucle d'hystérésis - {tension}")
    ax_hys.grid(True)
    ax_hys.legend()

    plt.tight_layout()
    i += 1
    plt.savefig(f"{i}_{tension}.png")
    plt.close()
