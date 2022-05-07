import sqlite3, pandas as pd
import numpy as np, matplotlib.pyplot as plt
import string, math


#Create n random cities with x and y coordinates between 0 and 100 and store them in lists X and Y as integers
print("How many cities would you like to generate? (Maximum of 676)")
n = int(input())

X = np.random.uniform(0,100,n)
X = [int(k) for k in X]
Y = np.random.uniform(0,100,n)
Y = [int(k) for k in Y]

#Generate a list of names (aa, ab, ac, ..., zz) and cut it to the size of the number of cities created
double_alphabet = [char + char2 for char in string.ascii_lowercase for char2 in string.ascii_lowercase]
names = [double_alphabet[x] for x in range(0,n)]

#Find the distance from each city to every other city, and store it in the distance_grid list
distance_grid = []
for i in range(0,len(names)):
    temp = []
    for k in range(0,len(names)):
        distance = int(math.sqrt((X[k] - X[i])**2 + (Y[k] - Y[i])**2))
        temp.append(distance)
    distance_grid.append(temp)

#Turn the distance_grid into text so it can be stored using an sql database
distance_grid_txt = []
for i in distance_grid:
    temp = ""
    for num in i:
        temp += str(num) + ","
    temp = temp[:-1]
    distance_grid_txt.append(temp)

#Connect and setup database
conn = sqlite3.connect('TSP Problem')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS Cities
    (Names TEXT,
    XCoords INT,
    YCoords INT,
    Distances TEXT);""")
c.execute("DELETE FROM Cities")
conn.commit()

#Insert data into the database
for i in range(0,n):
    conn.execute("INSERT INTO Cities (Names, XCoords, YCoords, Distances) VALUES (?, ?, ?, ?)", (names[i], X[i], Y[i], distance_grid_txt[i]));
conn.commit()

#Print and close the table
df = pd.read_sql_query("SELECT * from Cities", conn)
print(df)
conn.close()

plt.scatter(X,Y)
plt.show()
