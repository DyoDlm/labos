import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cv2

#   read data...
data = pd.read_csv('results.csv')
x_coords = data['X'].values
y_coords = data['Y'].values

#   manual placement... 
foyer1 = (207, 75)  # Foyer gauche
foyer2 = (209, 275)  # Foyer droit

def generate_hyperbola(foyer1, foyer2, a):
    c = np.sqrt((foyer2[0] - foyer1[0])**2 + (foyer2[1] - foyer1[1])**2) / 2
    b = np.sqrt(c**2 - a**2)
    h = (foyer1[0] + foyer2[0]) / 2
    k = (foyer1[1] + foyer2[1]) / 2

    x = np.linspace(0, width, 500)
    y_upper = k + b * np.sqrt(1 + ((x - h) / a) ** 2)
    y_lower = k - b * np.sqrt(1 + ((x - h) / a) ** 2)

    return x, y_upper, y_lower


#   graphic plot section...
plt.figure(figsize=(12, 8))
plt.imshow(image_rgb, extent=[0, width, height, 0])
plt.scatter(x_coords, y_coords, c='red', s=30, label='Maxima détectés')
plt.xlim(int(min(x_coords)), int(max(x_coords)))
plt.ylim(int(min(y_coords)), int(max(y_coords)))
plt.scatter([foyer1[0], foyer2[0]], [foyer1[1], foyer2[1]], c='blue', s=100, marker='x', label='Foyers')

a_values = np.linspace(30, 80, 30)
for a in a_values:
    x, y_upper, y_lower = generate_hyperbola(foyer1, foyer2, a)
    plt.plot(x, y_upper, 'b-', linewidth=1, alpha=0.5)
    plt.plot(x, y_lower, 'g-', linewidth=1, alpha=0.5)

plt.xlabel('Position X \\ pixels')
plt.ylabel('Position Y \\ pixels')
plt.legend(loc='upper right')
plt.savefig('interferences_with_hyperboles.png', dpi=300, bbox_inches='tight')
plt.close()

