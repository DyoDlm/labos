import numpy as np
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

# ============================================================
# BOUCLE PRINCIPALE
# ============================================================
for tension, files in groups.items():
    # ========================================================
    # FIGURE HYSTERESE (une figure par tension)
    # ========================================================
    fig_hys, ax_hys = plt.subplots(figsize=(8, 6))

    # ========================================================
    # PARCOURS DES FICHIERS (par fréquence)
    # ========================================================
    for file in files:
        # ----------------------------------------------------
        # Lecture CSV
        # ----------------------------------------------------
        df = pd.read_csv(file, skiprows=2)

        # ----------------------------------------------------
        # Colonnes
        # ----------------------------------------------------
        time = df.iloc[:, 0].values
        canal_A = df.iloc[:, 1].values
        canal_B = df.iloc[:, 2].values / 1000  # mV -> V

        # ----------------------------------------------------
        # Extraction fréquence depuis nom fichier
        # ----------------------------------------------------
        if "5Hz" in file:
            freq = "5 Hz"
        elif "10Hz" in file:
            freq = "10 Hz"
        elif "20Hz" in file:
            freq = "20 Hz"
        else:
            freq = "?"

        # ====================================================
        # COURBE D'HYSTERESE (par fréquence)
        # ====================================================
        ax_hys.plot(canal_A, canal_B, linewidth=1.5, label=freq)

        # ========================================================
        # CALCUL DE AB, CD ET COEFFICIENT DE NON-LINÉARITÉ POUR CETTE FRÉQUENCE
        # ========================================================
        # Convertir en tableaux numpy
        canal_A_array = np.array(canal_A)
        canal_B_array = np.array(canal_B)

        # Trouver les indices des points A (min) et B (max) en déplacement
        idx_A = np.argmin(canal_B_array)
        idx_B = np.argmax(canal_B_array)

        # Coordonnées de A et B
        A = (canal_A_array[idx_A], canal_B_array[idx_A])
        B = (canal_A_array[idx_B], canal_B_array[idx_B])

        # Calcul de AB (déplacement total)
        AB = B[1] - A[1]

        # ========================================================
        # CALCUL DE CD (Écart maximal par rapport à la droite AB)
        # ========================================================
        if B[0] != A[0]:  # Éviter la division par zéro
            m = (B[1] - A[1]) / (B[0] - A[0])
            b = A[1] - m * A[0]

            # Calculer les déplacements théoriques (sur la droite AB)
            theoretical_B = m * canal_A_array + b

            # Calculer les écarts signés
            deviations_signed = canal_B_array - theoretical_B

            # Trouver les indices des écarts maximaux (positif et négatif)
            idx_C = np.argmax(deviations_signed)  # Point au-dessus de la droite
            idx_D = np.argmin(deviations_signed)  # Point en dessous de la droite

            C = (canal_A_array[idx_C], canal_B_array[idx_C])
            D = (canal_A_array[idx_D], canal_B_array[idx_D])

            # Calcul de CD (écart maximal)
            CD = np.abs(C[1] - D[1])
        else:
            # Cas où A et B ont la même tension (droite verticale)
            CD = 0
            C = A
            D = B

        # ========================================================
        # CALCUL DU COEFFICIENT DE NON-LINÉARITÉ
        # ========================================================
        if AB != 0:
            non_linearity_coefficient = CD / AB
        else:
            non_linearity_coefficient = 0

        # ========================================================
        # AFFICHAGE DES RÉSULTATS POUR CETTE FRÉQUENCE
        # ========================================================
        print(f"\n--- Tension : {tension}, Fréquence : {freq} ---")
        print(f"Point A (min) : {A}")
        print(f"Point B (max) : {B}")
        print(f"AB (déplacement total) : {AB:.3f} V")
        print(f"Point C (écart max +) : {C}")
        print(f"Point D (écart max -) : {D}")
        print(f"CD (écart maximal) : {CD:.3f} V")
        print(f"Coefficient de non-linéarité (CD/AB) : {non_linearity_coefficient:.3f}")

        # ========================================================
        # TRAÇAGE DE LA DROITE AB ET DES POINTS C, D POUR CETTE FRÉQUENCE
        # ========================================================
        # Tracer la droite AB
        x_ab = np.array([A[0], B[0]])
        y_ab = np.array([A[1], B[1]])
        ax_hys.plot(x_ab, y_ab, 'k--', linewidth=1, alpha=0.5)

        # Marquer les points A, B, C, D
        ax_hys.scatter([A[0], B[0]], [A[1], B[1]], color='red', s=50, zorder=5)
        ax_hys.scatter([C[0], D[0]], [C[1], D[1]], color='blue', s=50, zorder=5)

    # ========================================================
    # FINALISATION DES FIGURES
    # ========================================================
    ax_hys.set_xlabel("Tension (V)")
    ax_hys.set_ylabel("Déplacement (V)")
    ax_hys.set_title(f"Boucle d'hystérésis - {tension}")
    ax_hys.grid(True)
    ax_hys.legend()

    plt.tight_layout()
    i += 1
    plt.savefig(str(i) + "_" + tension + ".png")
    plt.close()  # Fermer la figure pour éviter la superposition
