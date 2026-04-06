import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cv2


SCALE_FACTOR = 17

data = pd.read_csv('results.csv')
x_coords = data['X'].values
y_coords = data['Y'].values

height = 10
width = 10 #image.shape[:2]

# Tracer les points sur l'image pour visualiser les foyers
plt.figure(figsize=(12, 8))
plt.scatter(x_coords/SCALE_FACTOR, y_coords/SCALE_FACTOR, c='red', s=30, label='Maxima détectés')
plt.title("Maxima détectés par ImageJ")
plt.xlabel('Position X (pixels)')
plt.ylabel('Position Y (pixels)')
plt.legend()
plt.savefig('maxima_scaled_plot.png', dpi=300, bbox_inches='tight')
plt.close()

foyer1 = (221, 122)  # Foyer gauche
foyer2 = (222, 198)  # Foyer droit

# Fonction pour générer des points d'une hyperbole
def generate_hyperbola(foyer1, foyer2, a):
    c = np.sqrt((foyer2[0] - foyer1[0])**2 + (foyer2[1] - foyer1[1])**2) / 2
    b = np.sqrt(c**2 - a**2)
    h = (foyer1[0] + foyer2[0]) / 2
    k = (foyer1[1] + foyer2[1]) / 2

    x = np.linspace(0, width, 500)
    y_upper = k + b * np.sqrt(1 + ((x - h) / a) ** 2)
    y_lower = k - b * np.sqrt(1 + ((x - h) / a) ** 2)

    return x, y_upper, y_lower


# Tracer les hyperboles
plt.figure(figsize=(12, 8))
#plt.imshow(image_rgb, extent=[0, width, height, 0])
plt.scatter(x_coords/SCALE_FACTOR, y_coords/SCALE_FACTOR, c='red', s=30, label='Maxima détectés')
plt.xlim(0, 40)
plt.ylim(0, 40)
# Tracer les foyers
plt.scatter([foyer1[0]/SCALE_FACTOR, foyer2[0]/SCALE_FACTOR],
            [foyer1[1]/SCALE_FACTOR, foyer2[1]/SCALE_FACTOR],
            c='blue', s=100, marker='x', label='Foyers')

# Tracer une série d'hyperboles avec différentes valeurs de a
a_values = np.linspace(3, 20, 10)  # Différentes valeurs de a pour tracer plusieurs hyperboles
for a in a_values:
    x, y_upper, y_lower = generate_hyperbola(foyer1, foyer2, a)
    plt.plot(x, y_upper/SCALE_FACTOR, 'b-', linewidth=1, alpha=0.5)
    plt.plot(x, y_lower/SCALE_FACTOR, 'g-', linewidth=1, alpha=0.5)

plt.title("Hyperboles tracées sur les interférences")
plt.xlabel('Position X (pixels)')
plt.ylabel('Position Y (pixels)')
plt.legend()
plt.savefig('interferences_with_scaled_hyperboles.png', dpi=300, bbox_inches='tight')
plt.close()
