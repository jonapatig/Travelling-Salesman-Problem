import sqlite3, pandas as pd
import numpy as np, matplotlib.pyplot as plt
import random

################################################################################
#RETRIEVING AND NORMALIZING DATA FROM THE DATABASE
###############################################################################
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

################################################################################
#DECLARING CRUCIAL INITIAL VALUES. CAN BE EDITED TO ALTER PROGRAM
###############################################################################
popSize = 100 #declare the initial size of the population
mutation_rate = 20 #declare a % integer (20 --> 20% likelihood to mutate per city in tour)
population = []
lengths, fitnesses = [], []
termination_condition = 20
bestEver = 999999999

################################################################################
#CREATING ALL CRUCIAL FUNCTIONS OF THE GENETIC ALGORITHM
###############################################################################
#Generate Inital Population
def generate_population(popSize, where):
    for i in range(0, popSize):
        copy = names.copy()
        tour = []
        for k in range(0,len(names)):
            x = random.randint(0,len(copy)-1)
            tour.append(copy[x])
            copy.pop(x)
        where.append(tour)

#Determine total lengths and fitnesses of all tours in the population
def determine_lengths(generation):
    global lengths, fitnesses, bestEver
    lengths, fitnesses = [], []
    for tour in generation:
        length = 0
        for city in tour:
            if not city == tour[-1]:
                length += distance_grid[names.index(city)][names.index(tour[tour.index(city)+1])]
            else:
                length += distance_grid[names.index(city)][names.index(tour[0])]
        lengths.append(length)
    for i in lengths:
        fitnesses.append(1/i*i)
    best = min(lengths)
    if best < bestEver:
        bestEver = best


#Roulette Wheel Selection
def roulette_wheel_selection(group,number):
    total = sum(fitnesses)
    probabilities = []
    positions = range(0,len(group))
    for i in fitnesses:
        probability = i/total
        probabilities.append(probability)
    chosen_indices = np.random.choice(positions, number, p=probabilities)
    chosen = []
    for i in chosen_indices:
        chosen.append(group[i])
    return chosen

#Mutation
def mutate(tour, rate):
    for i in range(0,len(tour)):
        if random.randint(0,100) <= rate:
            spot = random.randint(0,2)
            if not i+spot >= len(tour):
                temp = tour[i]
                tour[i] = tour[i+spot]
                tour[i+spot] = temp
            else:
                temp = tour[i]
                tour[i] = tour[i-spot]
                tour[i-spot] = temp
    return tour

#Cycle Crossover
def cycle_crossover(parent1, parent2):
    offspring1 = ['x' for i in range(0,len(parent1))]
    #First parent cycle
    start = 0
    marked1 = [parent1[0]]
    if not parent2.index(parent1[0]) == parent1.index(parent1[0]):
        current = parent1[parent2.index(parent1[0])]
        while not current == parent1[0]:
            marked1.append(current)
            current = parent1[parent2.index(current)]
    for k in range(0, len(marked1)):
        if not k == len(marked1)-1:
            offspring1[parent1.index(marked1[k])] = parent1[parent1.index(marked1[k+1])]
        else:
            offspring1[parent1.index(marked1[k])] = parent1[parent1.index(marked1[0])]
    for i in range(0,len(offspring1)):
        if offspring1[i] == 'x':
            offspring1[i] = parent1[i]
    return offspring1

def generate_new_generation(old_generation):
    global population
    new_population = []
    for i in population:
        parents = []
        selected = roulette_wheel_selection(old_generation, 2)
        mutated_parent1 = mutate(selected[0], mutation_rate)
        mutated_parent2 = mutate(selected[1], mutation_rate)
        new_population.append(cycle_crossover(mutated_parent1, mutated_parent2))
    population = new_population.copy()
################################################################################
#ACTUALLY RUNNING THE GENETIC ALGORITHM
###############################################################################
generate_population(popSize, population)
# determine_lengths(population)
# generate_new_generation(population)

no_change = 0
while no_change < termination_condition:
    determine_lengths(population)
    generate_new_generation(population)
    print(bestEver)



#Keep best for next generation(elitism)

################################################################################
#To do:
#-Do all the calculations, find the optimal order of names
#-Use index of names to draw lines and labels on the plot
