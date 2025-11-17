#!/env/py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_clean_content(file):
    print("extracting content", "\n")
    df = pd.read_csv(file)
    return df


def find_maximums(df):
    print("Finding maximums", "\n")
    x = df[df.columns[0]]
    y = df[df.columns[1]]

    cursor = 0
    first_max = 0
    for value in x:
        if value > first_max:
            first_max = value
            index = cursor
        cursor += 1

    tmax1 = y[index]
    
    second_max = 0
    index2 = 0
    cursor = 0
    for value in x:
        if index > 0:
            index -= 0.5
            cursor += 1
            continue
        if value > second_max:
            second_max = value
            index2 = cursor
        cursor += 1 
    
    tmax2 = y[index2]
        

    theta_max = [first_max, second_max]
    time_max = [tmax1, tmax2]
    return theta_max, time_max

def find_lambda(array):
    print("finding lambda")
    pseudo_period = array[0] - array[1]
    return pseudo_period

files=["Mesure_0_1A.csv", "Mesure_0_2A.csv", "Mesure_0_3A.csv", "Mesure_0_4A.csv", "Mesure_0_5A.csv"] #"Mesure_0_9A.csv"]

i = 0
amperes = [0.1,0.2,0.3,0.4,0.5]#,9]
lambda_arr = []
for file in files:
    i += 1
    df = get_clean_content(file)
    theta_maximums, time_maxs = find_maximums(df)
    print(f"For {amperes[i - 1]} amperes, maximums are : {theta_maximums}")
    print(f"times_intervals : {time_maxs}")
    pseudo_period = find_lambda(time_maxs)
    print(f"pseudo_period for {amperes[i - 1]} A is : {pseudo_period}")
    lambda_arr.append(pseudo_period)

#   now plot that shit
x = amperes
y = lambda_arr

plt.figure()
plt.xlabel('I [A]')
plt.ylabel('Lambda [1/Hz]')

plt.scatter(x, y)

plt.show()
