import matplotlib.pyplot as plt
import control as ctrl
import numpy as np

# Définir les fonctions de transfert
s = ctrl.TransferFunction.s
G_mot = 4.53e3 / (1 + s * 8e-3)
G_ele = 20.8e-3 / (1 + s * 1.5e-4)
G_mes = 10.7e-3

# Produit G_ele * G_mot
G_ele_mot = G_ele * G_mot

# Tracer
plt.figure(figsize=(10, 6))
ctrl.bode_plot(G_ele_mot, label="$G_{ele}(s) \\cdot G_{mot}(s)$", color="blue")
plt.legend()
plt.title("Comparaison : $G_{ele}(s) \\cdot G_{mot}(s)$")
plt.grid()
#plt.show()
plt.savefig("a.png")

#####################################################
#   B   #
####################################################
# Fonction de transfert complète
G_s = G_ele_mot * G_mes

# Tracer le diagramme de Bode
plt.figure(figsize=(10, 6))
ctrl.bode_plot(G_s, label="$G_s(s)$", color="red")
plt.legend()
plt.title("Diagramme de Bode de $G_s(s)$")
plt.grid()
#plt.show()
plt.savefig("b.png")
######################################################
#   C 
######################################################

######################################################
#   D 
######################################################
## Régulateur PI
k_R = 3306
T_n = 8e-3
G_R = k_R * (1 + s * T_n) / s

# Fonction de transfert en boucle ouverte
G_0 = G_R * G_s

# Fonction de transfert en boucle fermée
G_cf = ctrl.feedback(G_0, 1)

# Tracer la réponse indicielle
plt.figure(figsize=(10, 6))
t, y = ctrl.step_response(G_cf)
plt.plot(t, y, label="$G_{cf}(s)$")
plt.title("Réponse indicielle de $G_{cf}(s)$")
plt.xlabel("Temps [s]")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()
#plt.show()
plt.savefig("d.png")

######################################################
#   E 
######################################################
#
# Diagramme de Bode de G_0(s)
plt.figure(figsize=(10, 6))
ctrl.bode_plot(G_0, label="$G_0(s)$", color="green")
plt.legend()
plt.title("Diagramme de Bode de $G_0(s)$")
plt.grid()
#plt.show()
plt.savefig("e_bode.png")

# Diagramme de Nyquist de G_0(s)
plt.figure(figsize=(10, 6))
ctrl.nyquist_plot(G_0, label="$G_0(s)$", color="purple")
plt.legend()
plt.title("Diagramme de Nyquist de $G_0(s)$")
plt.grid()
#plt.show()
plt.savefig("e_nyquist.png")

######################################################
#   F 
######################################################
#
# Diagramme d'Evans (lieu des racines)
plt.figure(figsize=(10, 6))
ctrl.root_locus(G_0, grid=True)
plt.title("Diagramme d'Evans de $G_0(s)$")
plt.grid()
plt.show()
plt.savefig("f_evans.png")

# Réponse indicielle de G_cf(s)
plt.figure(figsize=(10, 6))
t, y = ctrl.step_response(G_cf)
plt.plot(t, y, label="$G_{cf}(s)$")
plt.title("Réponse indicielle de $G_{cf}(s)$")
plt.xlabel("Temps [s]")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()
#plt.show()
plt.savefig("f_indiciel.png")

######################################################
#   G 
######################################################
#   No graph



######################################################
#   H 
######################################################
#   No graph


######################################################
#   I 
######################################################
#

# Calcul des marges de stabilité
gm, pm, wg, wp = ctrl.margin(G_0)

print(f"Marge de gain : {gm:.2f} dB")
print(f"Marge de phase : {pm:.2f}° à {wp:.2f} rad/s")

# Tracer avec marges
plt.figure(figsize=(10, 6))
ctrl.bode_plot(G_0, label="$G_0(s)$", color="orange")
plt.legend()
plt.title("Diagramme de Bode avec marges de stabilité")
plt.grid()
#plt.show()
plt.savefig("i.png")

######################################################
#   J 
######################################################
#
# Ajouter un critère de dépassement de 5%
# Tracer le lieu des racines avec une zone de dépassement
plt.figure(figsize=(10, 6))
ctrl.root_locus(G_0, grid=True)
plt.title("Lieu des racines avec critère de dépassement de 5%")
plt.grid()
#plt.show()
plt.savefig("j.png")

######################################################
#   K 
######################################################
#
# Tracer la réponse indicielle avec annotations
plt.figure(figsize=(10, 6))
t, y = ctrl.step_response(G_cf)
plt.plot(t, y, label="$G_{cf}(s)$")
plt.savefig("k.png")


# Annoter le dépassement, temps de montée, etc.
peak = np.max(y)
overshoot = (peak - y[-1]) / y[-1] * 100
plt.annotate(f"Dépassement : {overshoot:.1f}%", xy=(t[np.argmax(y)], peak), xytext=(0.5, 0.9), arrowprops=dict(facecolor='black', shrink=0.05))

plt.title("Réponse indicielle avec caractéristiques")
plt.xlabel("Temps [s]")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()
#plt.show()
plt.savefig("k_data.png")

######################################################
#   L 
######################################################
#
# Tester différents gains k_R
k_R_values = [1000, 3306, 5000]

plt.figure(figsize=(10, 6))
for k in k_R_values:
    G_R = k * (1 + s * T_n) / s
    G_0 = G_R * G_s
    G_cf = ctrl.feedback(G_0, 1)
    t, y = ctrl.step_response(G_cf)
    plt.plot(t, y, label=f"$k_R = {k}$")

plt.title("Impact du gain $k_R$ sur la réponse indicielle")
plt.xlabel("Temps [s]")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()
#plt.show()
plt.savefig("l.png")

######################################################
#   M 
######################################################
## Tracer les diagrammes de Bode pour différents gains
plt.figure(figsize=(10, 6))
for k in k_R_values:
    G_R = k * (1 + s * T_n) / s
    G_0 = G_R * G_s
    ctrl.bode_plot(G_0, label=f"$k_R = {k}$")

plt.title("Stabilité pour différents gains $k_R$")
plt.grid()
plt.legend()
#plt.show()
plt.savefig("m.png")
