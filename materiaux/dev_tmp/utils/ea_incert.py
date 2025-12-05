import numpy as np
import matplotlib.pyplot as plt

x = [1,2,5,10,20]
y = [140.5, 143.5, 148.6,150.5,155.7]
incert = [1.606, 1.594, 1.601, 1.616, 1.518]

mid = 0
for item in incert:
    mid += item

mid /= len(incert)

print(f"Moyenne d'incertitudes : {mid}")
i = 0
for item in y:
    y[i] = 1/item 
    i += 1

i = 0
for item in x:
    x[i] = np.log(item)
    i += 1

fit = np.polyfit(y, x, 1)

poly = np.poly1d(fit, x, 1)

yfit = [0,0,0,0,0]
i = 0
for item in x:
    yfit[i] = poly(x[i])
    i += 1

print(f"Y fit is : {yfit}")

plt.figure()
plt.scatter(y, x, color='b')
plt.plot(x, yfit)
plt.grid()
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()

