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
l = [111.1,
     1179,
     308.8,
     910,
     263.6,
     187.4,
     1276,
     1173
        ]

dl = [0.2,
      5,
      0.5,
      2,
      0.4,
      0.3,
      6,
      3
        ]

def omega_0(omega_, lambda_):
    return np.sqrt(omega_*omega_ - lambda_*lambda_)

def domega_0(omega0, domega_, dlambda_, omega_, lambda_):
    return (1/omega0) * np.sqrt((omega_*domega_)**2 + (lambda_*dlambda_)**2)

t = [0,0,0,0,0,0,0,0]
dt = [0,0,0,0,0,0,0,0]
oo = [0,0,0,0,0,0,0,0]
doo = [0,0,0,0,0,0,0,0]
_iter = 0
for i in o:
    t[_iter] = 2* np.pi / i
    dt[_iter] = 2 * np.pi * do[_iter] / (i * i) 
    oo[_iter] = omega_0(i, l[_iter])
    doo[_iter] = domega_0(oo[_iter], do[_iter], dl[_iter], i, l[_iter])
    
    _iter += 1
print("period T [s]")
print(t)
print("delta period dT")
print(dt)
print("omega0 : ")
for i in oo:
    print(f"{i:.1f}")

print("")

print("Delta omega0 : ")
for i in doo:
    print(i)

