import numpy as np
import matplotlib.pyplot as plt

# Axe des x
x = np.linspace(0, 2*np.pi, 1000)

# Fonctions
y1 = np.cos(x) * 8
y2 = np.cos(x + np.pi/4) * 8
y3 = np.sin(x)
y4 = np.sin(x + np.pi/4)

# Figure
plt.figure(figsize=(8,5))

plt.plot(x, y1, label="deformation totale", linewidth=2)
plt.plot(x, y2, label="deformation elastique", linestyle="--")
plt.plot(x, y3, label="deformation visqueuse", linewidth=2)
plt.plot(x, y4, label="contrainte", linestyle="--")

# Mise en forme
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.legend()

plt.savefig("DMAexample.png")

