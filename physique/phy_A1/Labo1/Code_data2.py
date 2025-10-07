import numpy as np
import matplotlib.pyplot as plt
from pandas import read_excel 

def func_deg2(x,a,b,c):
    return a*x**2+b*x+c

def show_symb(val,showPlus=True):
    if showPlus and val >0: return '+'
    elif val <0: return '-'
    return ''

# Get datas
data = read_excel('data/data2.xlsx')
x = data[data.columns[0]]
y = data[data.columns[1]]  

# Fit datas
DatArr,cov = np.polyfit(x, y, 2, cov=True)
delta_voc = np.sqrt(np.diag(cov))

# Init plot
plt.figure()
plt.xlabel('x(unite)')
plt.ylabel('y(unite)')
plt.xlim(min(x)-2,max(x)+2)
plt.grid()

# Plot datas
plt.plot(x,y,"ro",label="Values")
plt.plot(x,func_deg2(x,DatArr[0],DatArr[1],DatArr[2]),"b-",label="Fit")
plt.legend()
#plt.text(-10, 3000, f"y=x$^2$*{show_symb(DatArr[0])}{DatArr[0]:.2f}+x*{show_symb(DatArr[1])}{DatArr[1]:.2f}{show_symb(DatArr[2])}{abs(DatArr[2]):.2f}")
plt.text(-10, 3000, f"y={show_symb(DatArr[1],False)}{abs(DatArr[0]):.2f}*x$^2${show_symb(DatArr[1],False)}{abs(DatArr[1]):.2f}*x{show_symb(DatArr[2])}{abs(DatArr[2]):.2f}")

plt.show()

# Show datas values
for i in range(len(DatArr)):
    print(f"Param {chr(ord('a')+i)} : {DatArr[i]:.2E} ± {delta_voc[i]:.2E}")



