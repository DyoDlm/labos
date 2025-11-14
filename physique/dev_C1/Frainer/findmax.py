#!/env/py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_clean_content(file):
    print("extracting content")
    df = pd.read_csv(file)
    return df


def find_maximums(df):
    print("Finding maximums")
    x = df[df.columns[0]]
    y = df[df.columns[1]]

    print(x, y)
    maximums = [1,2]
    return maximums

def find_minimums(df):
    print("Finding minimums")
    x = df[df.columns[0]]
    y = df[df.columns[1]]

    minimums = [1,2]
    return minimums

def find_lambda(array):
    print("finding lambda")
    pseudo_period = array[1] - array[0]
    return pseudo_period

files=["Mesure_0_1A.csv", "Mesure_0_2A.csv", "Mesure_0_3A.csv", "Mesure_0_4A.csv", "Mesure_0_5A.csv", "Mesure_0_9A.csv"]

i = 0
amperes = [1,2,3,4,5,9]
lambda_arr = []
for file in files:
    i += 1
    df = get_clean_content(file)
    maximums = find_maximums(df)
    minimums = find_minimums(df)
    print(f"For 0.{amperes[i - 1]} amperes, maximums are : {maximums}")
    pseudo_period = find_lambda(maximums)
    print(f"pseudo_period for 0.{amperes[i - 1]} A is : {pseudo_period}")
    lambda_arr.append(pseudo_period)

#   now plot that shit
x = amperes
y = lambda_arr

plt.figure()
plt.xlabel('I [A]')
plt.ylabel('Lambda [1/Hz]')

plt.plot(x, y)

plt.show()
