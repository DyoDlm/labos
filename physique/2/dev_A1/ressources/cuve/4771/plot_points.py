import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2

# Lire les données depuis le fichier CSV
data = pd.read_csv('results.csv')  # Remplacez par le chemin de votre fichier CSV

# Extraire les coordonnées X et Y
x_coords = data['X'].values
y_coords = data['Y'].values

# Charger l'image (optionnel, si vous voulez superposer les points sur l'image)
image_path = 'worked.png'  # Remplacez par le chemin de votre image
image = cv2.imread(image_path)
if image is not None:
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width = image.shape[:2]

# Créer le graphique
plt.figure(figsize=(12, 8))

# Si une image est chargée, l'afficher en arrière-plan
if image is not None:
    plt.imshow(image_rgb, extent=[0, width, height, 0])

i = 0
x = np.zeros(len(x_coords))
y = np.zeros(len(y_coords))

for e in x_coords:
    if e < 45:
        x[i] = 0
        y[i] = 0
    else:
        x[i] = e
    i += 1
i = 0

for e in y_coords:
    if e < 40:
        y[i] = 0
        x[i] = 0
    else:
        y[i] = e
    i += 1

x_coords = x
y_coords = y
# Tracer les points
plt.scatter(x_coords, y_coords, c='red', s=30, label='Maxima détectés')

# Ajouter des étiquettes et une légende
plt.title("Maxima détectés par ImageJ")
plt.xlabel('Position X (pixels)')
plt.ylabel('Position Y (pixels)')
plt.legend()

# Sauvegarder le graphique
plt.savefig('maxima_plot.png', dpi=300, bbox_inches='tight')
plt.close()

# Afficher les 10 premiers points pour vérification
print("Coordonnées des 10 premiers points :")
print(data[['X', 'Y']].head(10))
