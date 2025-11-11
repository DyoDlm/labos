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

def parse(df, param: str):
    status = 0
    new_tab = []
    array = []
    for line in df:
        if line == param:
            new_tab = []
            if status == 0:
                status == 1
            else:
                status = 0
        elif status == 1:
            new_tab.insert(1, line)
            print("New line in tab : ", line)
        if line == "nan":
            array.insert(1, new_tab)
            new_tab = []
            status = 0

#        new_tab.insert(1, line)
#        print(new_tab)
    return array

directory = ""
file = "phy_B1.csv"
df = pd.read_csv(file, sep=';')

phase           = df[df.columns[0]].to_numpy()
courant         = df[df.columns[1]].to_numpy()
tensionGen      = df[df.columns[2]].to_numpy()
tensionRee      = df[df.columns[3]].to_numpy()
frequence       = df[df.columns[4]].to_numpy()

#print("PHASE     : ", phase)
#print("COURANT   : ", courant)
#print("TENSION GEN : ", tensionGen)
#print("TENSION REE : ", tensionRee)
#print("FREQUENCE : ", frequence)

g_phase         = parse(phase, "Phase phi +/- 0,1 [deg]")
for i in g_phase:
    print("New phase : ", i)
exit()
g_courant       = parse(courant, "Courant I +/- 10 [mA]")
g_tensionGen    = parse(tensionGen, "Tension Vgen (pp)+/- Datasheet [V]")
g_tensionRee    = parse(tensionRee, "Tension Vreel (pp) +/-0.001 [V]")
g_frequence     = parse(frequence, "frequence [Hz]")

#df = pd.read_excel(directory + file, engine=".csv")#, engine=".ods")
for i in df[df.columns[0]].to_numpy():
    print(i)

print("COMPLETE DATAFRAME")
#print(df)
exit(1)

new = plot(df, "", file)
print(f"New file created : {new} !")

