import numpy as np
import cv2
import matplotlib.pyplot as plt

# ============================================================
# PARAMETRES INITIAUX
# ============================================================
threshold = 200  # Seuil d'intensité pour détecter les maxima
neighborhood_size = 20  # Taille du voisinage pour limiter à 1 maxima par bloc de 10x10 pixels
radius = 3  # Rayon des cercles pour les maxima
thickness = -1  # Épaisseur des cercles (-1 pour remplir)

# Taille cible pour l'image finale (après redimensionnement)
target_width, target_height = 800, 600

# Coordonnées des 4 points pour définir la ROI (x, y) :
# Format : [coin_sup_gauche, coin_sup_droit, coin_inf_gauche, coin_inf_droit]
roi_points = [
    (100, 50),   # Coin supérieur gauche (x, y)
    (500, 50),   # Coin supérieur droit (x, y)
    (100, 300),   # Coin inférieur gauche (x, y)
    (500, 300)    # Coin inférieur droit (x, y)
]

# Couleurs pour les maxima de chaque image (BGR)
# Une couleur par image (6 couleurs distinctes)
colors = [
    (0, 255, 0),     # Vert
    (255, 0, 0),     # Bleu
    (0, 0, 255),     # Rouge
    (0, 255, 255),   # Jaune
    (255, 0, 255),   # Magenta
    (255, 255, 0)    # Cyan
]

# Chemins des 6 images
image_paths = [
    "5V.jpg",
    "10V.jpg",
    "15V.jpg",
    "20V.jpg"
    ]##"25V.jpg",
#"30V.jpg"
#]

# ============================================================
# FONCTION POUR TROUVER LES MAXIMA AVEC LIMITATION DE VOISINAGE
# ============================================================
def find_local_maxima(image, threshold, neighborhood_size):
    max_pixels = np.argwhere(image > threshold)
    grid_size = neighborhood_size
    height, width = image.shape
    grid_y = np.arange(0, height, grid_size)
    grid_x = np.arange(0, width, grid_size)
    selected_maxima = []

    for y_start in grid_y:
        for x_start in grid_x:
            y_end = min(y_start + grid_size, height)
            x_end = min(x_start + grid_size, width)
            block = image[y_start:y_end, x_start:x_end]
            if block.size == 0:
                continue
            max_val = np.max(block)
            if max_val > threshold:
                max_pos_in_block = np.unravel_index(np.argmax(block), block.shape)
                y_abs = y_start + max_pos_in_block[0]
                x_abs = x_start + max_pos_in_block[1]
                selected_maxima.append((y_abs, x_abs))
    return selected_maxima

# ============================================================
# CHARGEMENT DES IMAGES ET DETECTION DES MAXIMA
# ============================================================
images = []
max_pixels_list = []

for path in image_paths:
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Erreur : l'image {path} n'a pas été trouvée.")
    images.append(image)
    max_pixels = find_local_maxima(image, threshold, neighborhood_size)
    max_pixels_list.append(max_pixels)

# ============================================================
# SUPERPOSITION DES MAXIMA SUR UNE IMAGE COULEUR
# ============================================================
# Utiliser la première image comme base pour la superposition
superposed_image = cv2.cvtColor(images[0], cv2.COLOR_GRAY2BGR)

# Superposer les maxima de chaque image avec sa couleur
for i, max_pixels in enumerate(max_pixels_list):
    color = colors[i]
    for (y, x) in max_pixels:
        cv2.circle(superposed_image, (x, y), radius, color, thickness)

# ============================================================
# REDIMENSIONNEMENT ET CENTRAGE DE L'IMAGE AVEC ROI
# ============================================================
# Extraire la ROI à partir des 4 points
x1, y1 = roi_points[0]  # Coin supérieur gauche
x2, y2 = roi_points[1]  # Coin supérieur droit
x3, y3 = roi_points[2]  # Coin inférieur gauche
x4, y4 = roi_points[3]  # Coin inférieur droit

# Calculer les dimensions de la ROI
roi_width = x2 - x1
roi_height = y4 - y1

# Extraire la ROI de superposed_image
roi = superposed_image[y1:y1 + roi_height, x1:x1 + roi_width]

# Redimensionner la ROI pour qu'elle tienne dans target_width x target_height
resized_roi = cv2.resize(roi, (target_width, target_height), interpolation=cv2.INTER_LINEAR)

# Créer une image noire de la taille cible
centered_image = np.zeros((target_height, target_width, 3), dtype=np.uint8)

# Placer la ROI redimensionnée au centre de centered_image
centered_image[:target_height, :target_width] = resized_roi

# Remplacer superposed_image par centered_image pour la suite
superposed_image = centered_image

# ============================================================
# AFFICHAGE
# ============================================================
plt.figure(figsize=(18, 6))

# Afficher les 6 images originales
for i, image in enumerate(images):
    plt.subplot(2, 4, i + 1)
    plt.imshow(image, cmap="gray")
    plt.title(f"Image {i + 1} (originale)")

# Afficher la superposition
plt.subplot(2, 4, 7)
plt.imshow(cv2.cvtColor(superposed_image, cv2.COLOR_BGR2RGB))
plt.title(f"Superposition (Maxima > {threshold})")

plt.tight_layout()
plt.show()

# ============================================================
# SAUVEGARDE
# ============================================================
output_path = "superposition_6_images_centered_roi.png"
cv2.imwrite(output_path, superposed_image)
print(f"Image sauvegardée : {output_path}")
