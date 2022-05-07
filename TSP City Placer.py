import sqlite3, pandas as pd
import numpy as np, matplotlib.pyplot as plt
import string, math

print("How many cities would you like to generate? (Maximum of 676)")
n = int(input())

X = np.random.uniform(0,100,n)
X = [int(k) for k in X]
Y = np.random.uniform(0,100,n)
Y = [int(k) for k in Y]

print(X)

double_alphabet = [char + char2 for char in string.ascii_lowercase for char2 in string.ascii_lowercase]
names = [double_alphabet[x] for x in range(0,n)]

distance_grid = []

for i in range(0,len(names)):
    temp = []
    for k in range(0,len(names)):
        distance = int(math.sqrt((X[k] - X[i])**2 + (Y[k] - Y[i])**2))
        temp.append(distance)
    distance_grid.append(temp)

plt.scatter(X,Y)
plt.show()

#To do:
#-Store info to access on other py file
#-Do all the calculations, find the optimal order of names
#-Use index of names to draw lines and labels on the plot
