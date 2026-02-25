import numpy as np
import matplotlib.pyplot as plt
from pandas import read_excel
from scipy.optimize import curve_fit

def func_deg2(x,a,b,c):
    return a*x**2+b*x+c

def show_symb_val(val,showPlus=False):
    if showPlus and val >0: return f"+{abs(val):.2f}"
    elif val <0: return f"-{abs(val):.2f}"
    return f"{abs(val):.2f}"

def curve_func(x, a, b, c):
    return (a+b*x)*np.e**(-c*x)
    

# Get datas
data = read_excel('data/data3.xlsx',skiprows=600)
x = data[data.columns[0]]
y = data[data.columns[1]]  

# Fit datas
DatArr, cov = curve_fit(curve_func,x, y)
delta_voc = np.sqrt(np.diag(cov))

# Init plot
plt.figure()
plt.xlabel('x(unite)')
plt.ylabel('y(unite)')
plt.xlim(min(x),max(x))
plt.grid()

# Plot datas
plt.plot(x,y,"ro",label="Values")
plt.plot(x,curve_func(x,DatArr[0], DatArr[1], DatArr[2]),"b-",label="Fit")
plt.legend()
#plt.text(np.mean(x)-0.01, np.mean(y)+2, f"y={show_symb_val(DatArr[1])}{abs(DatArr[0]):.2f}*x$^2${show_symb(DatArr[1])}{abs(DatArr[1]):.2f}*x{show_symb(DatArr[2],True)}{abs(DatArr[2]):.2f}")
plt.text(np.mean(x)-0.01, np.mean(y)+2, f"y=({show_symb_val(DatArr[0])}{show_symb_val(DatArr[1])}")
plt.show()

# Show datas values
for i in range(len(DatArr)):
    print(f"Param {chr(ord('a')+i)} : {DatArr[i]:.2E} ± {delta_voc[i]:.2E}")



