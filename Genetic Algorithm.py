import sqlite3, pandas as pd
import numpy as np, matplotlib.pyplot as plt
import random

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
population = []
copy = names

for i in range(0, popSize):
    copy = names.copy()
    tour = []
    for k in range(0,len(names)):
        x = random.randint(0,len(copy)-1)
        tour.append(copy[x])
        copy.pop(x)
    population.append(tour)

#Determine total lengths and fitnessesof all tours in the population
lengths, fitnesses = [], []

def determine_lengths():
    global lengths, fitnesses
    lengths, fitnesses = [], []
    for tour in population:
        length = 0
        for city in tour:
            if not city == tour[-1]:
                length += distance_grid[names.index(city)][names.index(tour[tour.index(city)+1])]
            else:
                length += distance_grid[names.index(city)][names.index(tour[0])]
        lengths.append(length)
    for i in lengths:
        fitnesses.append(1/i)

#Roulette Wheel Selection
def roulette_wheel_selection(pop,number):
    global fitnesses, lenghts
    total = sum(fitnesses)
    probabilities = []
    positions = range(0,len(pop))
    for i in fitnesses:
        probability = i/total
        probabilities.append(probability)
    chosen_indices = np.random.choice(positions, number, p=probabilities)
    chosen, chosen_lengths = [], []
    for i in chosen_indices:
        chosen.append(pop[i])
    return chosen


determine_lengths()
print(roulette_wheel_selection(population, 2))


################################################################################
#To do:
#-Do all the calculations, find the optimal order of names
#-Use index of names to draw lines and labels on the plot
