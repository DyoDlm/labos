import matplotlib.pyplot as plt
from pandas import read_csv


if __name__ == "__main__":
        

    # def linear(x,a,b):
    #     return a*x+b

    # Get datas
    data = read_csv('a/egale_0.csv')
    x = data[data.columns[0]]
    y = data[data.columns[1]]
    # # Fit datas
    # DatArr,cov = np.polyfit(x, y, 1, cov=True)
    # delta_voc = np.sqrt(np.diag(cov))

    # # Init plot
    # plt.figure()
    # plt.xlabel('x(unite)')
    # plt.ylabel('y(unite)')
    # plt.xlim(min(x)-2,max(x)+2)
    # plt.grid()

    # Plot datas
    plt.plot(x,y,"ro",label="Values")
    # plt.plot(x,linear(x,DatArr[0],DatArr[1]),"b-",label="Fit")
    plt.legend()
    # plt.text(40, 250, f"y=x*{DatArr[0]:.2f}+{DatArr[1]:.2f}")
    plt.show()

    # Show datas values
    # print(f"Param a : {DatArr[0]:.2E} ± {delta_voc[0]:.2E}")
    # print(f"Param b : {DatArr[1]:.2E} ± {delta_voc[1]:.2E}")
