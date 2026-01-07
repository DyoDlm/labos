import latexify
import pandas as pd
import matplotlib.pyplot as plt

# Chemin vers le fichier TXT

def plot(that):
    file_path = that   # à adapter

    filename = "plot_" + that
# Lecture :
# - séparateur = virgule
# - on ignore la ligne des unités
    df = pd.read_csv(
        file_path,
        sep=",",
        skiprows=[1]
    )

# Conversion en numérique
    df = df.apply(pd.to_numeric, errors="coerce")

# Extraction des colonnes
    t = df["x-axis"]
    y1 = df["1"]
    y2 = df["2"]

    max1 = y1.max()
    max2 = y2.max()
    min1 = y1.min()
    min2 = y2.min()

    time = max1 - max2
    amplitude1 = max1 - min1
    amplitude2 = max2 - min2

    print("----------------------")
    print(f"Resistances are : {file_path}")
    print(f"max generateur 1 : {max1}")
    print(f"max cable 2 : {max2}")
    print(f"min generateur 1 : {min1}")
    print(f"min cable 2 : {min2}")
    print(f"amplitude generateur1 : {amplitude1}")
    print(f"amplitude cable2 : {amplitude2}")
    print(f"Time between : {time}")
    print("----------------------")


# Plot
    plt.figure()
    plt.plot(t, y1, label="CH 1 (generateur)")
    plt.plot(t, y2, label="CH 2 (cable coaxial)")

    plt.xlabel(r"Temps t \ $\mu$s" )
    plt.ylabel("Tension U \ V")
    plt.legend()
    plt.grid(True)
    name = file_path.split(".")
    plt.savefig(name[0])
    plt.show()

resistances = ["s1500_14.csv", "s2500_15.csv", "s40pe_11.csv","s15pe_6.csv", "s25pe_8.csv", "s500e_13.csv", "s100e_12.csv", "s2000_16.csv", "s30pe_9.csv", "s5ope_4.csv", "s10pe_5.csv","s20pe_7.csv", "s35pe_10.csv"]

for i in resistances:
    print(i)
    plot(i)
    print("res was ploted")
