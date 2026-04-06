import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cv2

# Charger les données des points détectés
data = pd.read_csv('results.csv')
x_coords = data['X'].values
y_coords = data['Y'].values

# Charger l'image
image_path = 'worked.png'
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
height, width = image.shape[:2]

# Tracer les points sur l'image pour visualiser les foyers
plt.figure(figsize=(12, 8))
plt.imshow(image_rgb, extent=[0, width, height, 0])
plt.scatter(x_coords, y_coords, c='red', s=30, label='Maxima détectés')
plt.title("Maxima détectés par ImageJ")
plt.xlabel('Position X (pixels)')
plt.ylabel('Position Y (pixels)')
plt.legend()
plt.savefig('maxima_plot.png', dpi=300, bbox_inches='tight')
plt.close()

# Identifier les foyers (ajustez ces valeurs en fonction de votre image)
foyer1 = (188, 99)  # Foyer gauche
foyer2 = (190, 175)  # Foyer droit

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
plt.imshow(image_rgb, extent=[0, width, height, 0])
plt.scatter(x_coords, y_coords, c='red', s=30, label='Maxima détectés')
plt.xlim(0, 400)
plt.ylim(0, 400)
# Tracer les foyers
plt.scatter([foyer1[0], foyer2[0]], [foyer1[1], foyer2[1]], c='blue', s=100, marker='x', label='Foyers')

# Tracer une série d'hyperboles avec différentes valeurs de a
a_values = np.linspace(30, 100, 20)  # Différentes valeurs de a pour tracer plusieurs hyperboles
print(a_values)
#a_values = np.array([80, 82, 84, 86])
#a_values = [40, 90, 110, 140]
for a in a_values:
    x, y_upper, y_lower = generate_hyperbola(foyer1, foyer2, a)
    plt.plot(x, y_upper, 'b-', linewidth=1, alpha=0.5)
    plt.plot(x, y_lower, 'g-', linewidth=1, alpha=0.5)

plt.title("Hyperboles tracées sur les interférences")
plt.xlabel('Position X (pixels)')
plt.ylabel('Position Y (pixels)')
plt.legend()
plt.savefig('interferences_with_hyperboles.png', dpi=300, bbox_inches='tight')
plt.close()
