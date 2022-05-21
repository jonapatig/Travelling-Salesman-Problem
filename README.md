# Travelling-Salesman-Problem
I decided to make my own little version of a genetic algorithm to solve the travelling salesman problem. The 2 main files are "TSP City Place.py" and "Genetic Algorithm.py". "TSP Problem" is just the sql database storing the generated city coordinates and distances. It's not really necessary, as the TSP City Placer will randomly generate, place, and create a new database of cities if it isn't there. 

Some variables can be edited within the Genetic Algorithm.py file. The TSP City Placer will take the number of citites as an input when it is run. 
These include:
- Population size
- Mutation rate
- Termination Condition

The non-native python libraries required for the program to run are:
- pandas
- numpy
- matplotlib
