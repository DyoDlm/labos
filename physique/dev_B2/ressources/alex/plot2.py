import matplotlib.pyplot as plt
import numpy as np
# 1/D
x = [0.00111 ,0.00097
,0.00093
,0.00090
,0.00085
,0.00081
,0.00078
,0.00071
,0.00067
,0.00063
,0.00059
,0.00053
,0.00050]

y = [0.200,
0.193,
0.180,
0.175,
0.169,
0.166,
0.160,
0.154,
0.144,
0.129,
0.129,
0.115,
0.110]

x2 = [0.00000123,
0.00000094,
0.00000087,
0.00000081,
0.00000073,
0.00000065,
0.00000061,
0.00000051,
0.00000044,
0.00000039,
0.00000035,
0.00000028,
0.00000025]

y2 = [0.0400,
0.0372,
0.0324,
0.0306,
0.0286,
0.0276,
0.0256,
0.0237,
0.0207,
0.0166,
0.0166,
0.0132,
0.0121]

x = x2
y = y2
def regression_lineaire(x, y):
    """
    Calcule la régression linéaire y = ax + b
    Retourne a (pente) et b (ordonnée à l'origine)
    """
    x = np.array(x)
    y = np.array(y)

    a, b = np.polyfit(x, y, 1)
    return a, b



plt.figure()

a, b = regression_lineaire(x, y)


# Droite de régression
x_droite = np.linspace(min(x), max(x), 100)
y_droite = a * x_droite + b
plt.plot(x_droite, y_droite, label=rf"$U^2$ = {a:.2f} * 1/$D^2$ + {b:.2f}")
plt.legend()
plt.scatter(x, y)
plt.xlabel(r"1/$D^2$ \ m ")
plt.ylabel(r"$U^2$ \ V")
plt.grid(True)
plt.savefig("acc2.png")
plt.show()

