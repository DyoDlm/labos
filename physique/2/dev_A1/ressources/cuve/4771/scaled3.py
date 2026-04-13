import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cv2

SCALE_FACTOR = 20

data = pd.read_csv('results.csv')
x_coords = data['X'].values
y_coords = data['Y'].values

# Tracer les points sur l'image pour visualiser les foyers
plt.figure(figsize=(12, 8))
plt.scatter(x_coords/SCALE_FACTOR, y_coords/SCALE_FACTOR, c='red', s=30, label='Maxima détectés')
plt.title("Maxima détectés par ImageJ")
plt.xlabel('Position X')
plt.ylabel('Position Y')
plt.legend()
plt.xlim(int(min(x_coords)/SCALE_FACTOR), int(max(x_coords)/SCALE_FACTOR))
plt.ylim(int(min(y_coords)/SCALE_FACTOR), int(max(y_coords)/SCALE_FACTOR))
print(int(max(y_coords)/SCALE_FACTOR))
plt.savefig('maxima_scaled_plot.png', dpi=300, bbox_inches='tight')
plt.close()
foyer1 = (188, 99)  # Foyer gauche
foyer2 = (190, 175)

# Fonction pour générer des points d'une hyperbole
def generate_hyperbola(foyer1, foyer2, a):
    c = np.sqrt((foyer2[0] - foyer1[0])**2 + (foyer2[1] - foyer1[1])**2) / 2
    if a >= c:
        a = c * 0.99  # Assure que a est légèrement inférieur à c
    b = np.sqrt(c**2 - a**2)
    h = (foyer1[0] + foyer2[0]) / 2
    k = (foyer1[1] + foyer2[1]) / 2

    x_min = min(x_coords)/SCALE_FACTOR - 5
    x_max = max(x_coords)/SCALE_FACTOR + 5
    x = np.linspace(x_min, x_max, 500)
    y_upper = k/SCALE_FACTOR + (b/SCALE_FACTOR) * np.sqrt(1 + ((x - h/SCALE_FACTOR) / (a/SCALE_FACTOR)) ** 2)
    y_lower = k/SCALE_FACTOR - (b/SCALE_FACTOR) * np.sqrt(1 + ((x - h/SCALE_FACTOR) / (a/SCALE_FACTOR)) ** 2)

    return x, y_upper, y_lower

# Tracer les hyperboles
plt.figure(figsize=(12, 8))
plt.scatter(x_coords/SCALE_FACTOR, y_coords/SCALE_FACTOR, c='red', s=30, label='Maxima détectés')

# Tracer les foyers
plt.scatter([foyer1[0]/SCALE_FACTOR, foyer2[0]/SCALE_FACTOR],
            [foyer1[1]/SCALE_FACTOR, foyer2[1]/SCALE_FACTOR],
            c='blue', s=100, marker='x', label='Foyers')

# Tracer une série d'hyperboles avec différentes valeurs de a
#a_values = np.linspace(30, 100, 20)
#print(a_values)
a_values = np.linspace(30, 180,40)  # Différentes valeurs de a pour tracer plusieurs hyperboles

for a in a_values:
    x, y_upper, y_lower = generate_hyperbola(foyer1, foyer2, a)
    plt.plot(x, y_upper, 'b-', linewidth=1, alpha=0.5)
    plt.plot(x, y_lower, 'g-', linewidth=1, alpha=0.5)

plt.xlabel('X \ mm')
plt.ylabel('Y \ mm')
plt.xlim(int(min(x_coords)/SCALE_FACTOR), int(max(x_coords)/SCALE_FACTOR))
plt.ylim(int(min(y_coords)/SCALE_FACTOR), int(max(y_coords)/SCALE_FACTOR))
plt.legend()
plt.savefig('4771_interferences_with_scaled_hyperboles.png', dpi=300, bbox_inches='tight')
plt.close()
