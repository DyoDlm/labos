import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_csv(file):
    """Load the CSV file and return a dataframe."""
    print(f"[INFO] Loading {file}")
    return pd.read_csv(file)


def find_max(df, start_index, interval):
    """
    Cherche le maximum dans df à partir de 'start_index' sur une fenêtre de taille 'interval'.
    
    Arguments :
        df : dataframe contenant temps et valeurs
        start_index : index de départ pour rechercher
        interval : taille de la fenêtre (estimation de la période)

    Retourne :
        (max_value, max_time, max_index)
    """
    t = df.iloc[:, 0].to_numpy()
    x = df.iloc[:, 1].to_numpy()

    # Déterminer les bornes
    end_index = min(start_index + interval, len(x))

    # Extraire la fenêtre
    window = x[start_index:end_index]

    # Trouver l’indice local du maximum
    local_idx = np.argmax(window)

    # Convertir vers l’indice global
    global_idx = start_index + local_idx

    return x[global_idx], t[global_idx], global_idx


def pseudo_period(t1, t2):
    """Retourne la pseudo-période |t2 - t1|."""
    return abs(t2 - t1)


# -------------------------
#        MAIN
# -------------------------

files = [
    "Mesure_0_1A.csv",
    "Mesure_0_2A.csv",
    "Mesure_0_3A.csv",
    "Mesure_0_4A.csv",
    "Mesure_0_5A.csv"
]

amperes = [0.1, 0.2, 0.3, 0.4, 0.5]
lambda_arr = []

# Choix de l’intervalle (échantillons)
interval = 200      # ← À ajuster selon votre série temporelle
start_index = 0     # ← point de départ initial

for I, f in zip(amperes, files):

    df = load_csv(f)

    # 1er maximum
    max1, t1, idx1 = find_max(df, start_index, interval)

    # 2e maximum, une période plus loin
    max2, t2, idx2 = find_max(df, idx1 + interval, interval)

    print(f"\n[INFO] I = {I} A")
    print(f"Max 1 : valeur={max1}, t={t1}, index={idx1}")
    print(f"Max 2 : valeur={max2}, t={t2}, index={idx2}")

    lam = pseudo_period(t1, t2)
    print(f"Pseudo-période : {lam}")

    lambda_arr.append(lam)

# --- Plot ---
plt.figure()
plt.scatter(amperes, lambda_arr, color="blue")
plt.xlabel("I [A]")
plt.ylabel("Pseudo-période [s]")
plt.title("Pseudo-période en fonction du courant")
plt.grid(True)
plt.show()

