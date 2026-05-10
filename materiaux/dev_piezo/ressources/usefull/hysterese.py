import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ============================================================
# MODELE LINEAIRE
# ============================================================

def linear_model(x, a, b):
    return a * x + b


# ============================================================
# CONFIGURATION DES FICHIERS
# ============================================================

groups = {
    "1V": [
        "1V5Hz_15.csv",
        "1V10Hz_15.csv",
        "1V20Hz_15.csv"
    ],
    "2V": [
        "2V5Hz_15.csv",
        "2V10Hz_15.csv",
        "2V20Hz_15.csv"
    ],
    "3V": [
        "3V5Hz_15.csv",
        "3V10Hz_15.csv"
    ]
}

# ============================================================
# BOUCLE PRINCIPALE
# ============================================================

for tension, files in groups.items():

    # ========================================================
    # FIGURE HYSTERESE
    # ========================================================

    fig_hys, ax_hys = plt.subplots(figsize=(8, 6))

    # ========================================================
    # FIGURE COURBES LINEAIRES
    # ========================================================

    fig_lin, ax_lin = plt.subplots(figsize=(8, 6))

    # ========================================================
    # PARCOURS DES FICHIERS
    # ========================================================

    for file in files:

        # ----------------------------------------------------
        # Lecture CSV
        # ----------------------------------------------------

        df = pd.read_csv(
            file,
            skiprows=2
        )

        # ----------------------------------------------------
        # Colonnes
        # ----------------------------------------------------

        time = df.iloc[:, 0].values
        canal_A = df.iloc[:, 1].values
        canal_B = df.iloc[:, 2].values / 1000  # mV -> V

        # ----------------------------------------------------
        # Extraction fréquence
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
        # COURBE D'HYSTERESE
        # ====================================================

        ax_hys.plot(
            canal_A,
            canal_B,
            linewidth=1.5,
            label=freq
        )

        # ====================================================
        # REGRESSION LINEAIRE
        # ====================================================

        popt, _ = curve_fit(
            linear_model,
            canal_A,
            canal_B
        )

        a, b = popt

        x_fit = np.linspace(
            np.min(canal_A),
            np.max(canal_A),
            1000
        )

        y_fit = linear_model(x_fit, a, b)

        # ====================================================
        # COURBE LINEAIRE
        # ====================================================

        ax_lin.plot(
            x_fit,
            y_fit,
            linewidth=2,
            label=freq
        )

    # ========================================================
    # MISE EN FORME HYSTERESE
    # ========================================================

    ax_hys.set_title(
        f"Courbes d’hystérèse - {tension}"
    )

    ax_hys.set_xlabel("Canal A (V)")
    ax_hys.set_ylabel("Canal B (V)")

    ax_hys.grid(True)
    ax_hys.legend()

    fig_hys.tight_layout()

    # ========================================================
    # SAUVEGARDE HYSTERESE
    # ========================================================

    fig_hys.savefig(
        f"{tension}_hysterese.png",
        dpi=300
    )

    # ========================================================
    # MISE EN FORME COURBES LINEAIRES
    # ========================================================

    ax_lin.set_title(
        f"Régressions linéaires - {tension}"
    )

    ax_lin.set_xlabel("Canal A (V)")
    ax_lin.set_ylabel("Canal B (V)")

    ax_lin.grid(True)
    ax_lin.legend()

    fig_lin.tight_layout()

    # ========================================================
    # SAUVEGARDE COURBES LINEAIRES
    # ========================================================

    fig_lin.savefig(
        f"{tension}_lineaire.png",
        dpi=300
    )

    # ========================================================
    # FERMETURE FIGURES
    # ========================================================

    plt.close(fig_hys)
    plt.close(fig_lin)

print("Toutes les figures ont été sauvegardées.")
