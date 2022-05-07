import sqlite3, pandas as pd
import numpy as np, matplotlib.pyplot as plt

distance_grid, names, X, Y = [],[],[],[]
conn = sqlite3.connect('TSP Problem')
df = pd.read_sql_query("SELECT * from Cities", conn)

#Retrieving all data from the database
for i in df.index:
    distance_grid.append(df['Distances'].iloc[i].split(","))
    names.append(df['Names'].iloc[i])
    X.append(df['XCoords'].iloc[i])
    Y.append(df['YCoords'].iloc[i])

#Turn strings back to ints when retrieving distance data from database
temp2 = []
for i in distance_grid:
    temp1 = []
    for k in i:
        temp1.append(int(k))
    temp2.append(temp1)
distance_grid = temp2

#Generate Inital Population
popSize = 50



################################################################################
#To do:
#-Do all the calculations, find the optimal order of names
#-Use index of names to draw lines and labels on the plot
