import matplotlib.pyplot as plt
import pandas as pd


#   define raw data
#   it returns the new file name
#   somethings to do 
def plot(df, exp: str, name: str) -> str:
    tab = name.split('/')
    tab2 = tab[0].split(".csv")
    fileName = tab2[0] + "_plot"
    print(f"New file name : {fileName}")

    x = pd.to_numeric(df[df.columns[0]], errors='coerce')
    y = pd.to_numeric(df[df.columns[1]], errors='coerce')

    plt.grid()
    if exp == "a":
        #   afficher les valeurs de resistance sur le graph
        plt.title("Decharge d'un condensateur : Uc(t)")
        plt.ylabel("Volt +/- ? [V]")
        plt.xlabel("Time +/- ? [s]")
    elif exp == "e":
        #   determiner les parametres recherches
        plt.title("O")
        plt.ylabel("Volt +/- ? [V]")
        plt.xlabel("Time +/- ? [s]")
        facteur_amortissement = 0
        pseudo_periode = 0
    elif exp == "f":
        #   comparer avec valeurs theoriques
        plt.tinitial_paramsitle("")
        plt.ylabel("Volt +/- ? [V]")
        plt.xlabel("Time +/- ? [s]")
    else:
        plt.title("Tension en fonction de la frequence")
        plt.ylabel("")
        plt.xlabel("")

    plt.plot(x, y)
    plt.show()
    plt.savefig(fileName)
    return fileName


directory = ""
file = "phy_B1.csv"
df = pd.read_csv(file, sep=';')

phase=df[df.columns[0]].to_numpy())
courant=df[df.columns[1]].to_numpy())
tensionGen=df[df.columns[2]].to_numpy())
tensionRee=df[df.columns[3]].to_numpy())
frequence=df[df.columns[4]].to_numpy())

g_phase         = parse(phase)
g_courant       = parse(courant)
g_tensionGen    = parse(tensionGen)
g_tensionRee    = parse(frequence)

#df = pd.read_excel(directory + file, engine=".csv")#, engine=".ods")
for i in df[df.columns[0]].to_numpy():
    print(i)

print("COMPLETE DATAFRAME")
#print(df)
exit(1)

new = plot(df, "", file)
print(f"New file created : {new} !")

