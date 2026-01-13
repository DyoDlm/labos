import numpy as np

o= [
    3376.443,
    4512.171,
    7200.607,
    8894.358,
    5362.936,
    3381.811,
    7013.945,
    8875.445
]
do = [
    0.2,
    4.8,
    0.5,
    2.2,
    0.4,
    0.3,
    6.2,
    2.8
]

t = [0,0,0,0,0,0,0,0]
dt = [0,0,0,0,0,0,0,0]
_iter = 0
for i in o:
    t[_iter] = 2* np.pi / i
    dt[_iter] = 2 * np.pi * do[_iter] / (i * i) 
    _iter += 1
print("period T [s]")
print(t)
print("delta period dT")
print(dt)
