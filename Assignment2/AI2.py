# import statements for the random and csv modules.
import random
import csv


# Define the valid car models from the valid_book.csv file
valid_cars = set()
with open("Assignment2\Valid_book.csv", newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # row[0] = engine , row[1] = tire , row[2] = transmission , row[3] = roof
        valid_cars.add((row[0], row[1], row[2], row[3]))


# Define the available engine choices from the respective engines.txt files
with open('Assignment2\engines.txt', 'r') as f:
    engines = [line.strip() for line in f.readlines()]

# Define the available tire choices from the respective tires.txt files
with open('Assignment2\Tires.txt', 'r') as f:
    tires = [line.strip() for line in f.readlines()]

# Define the available transmission choices from the respective transmissions.txt files
with open('Assignment2\Transmissions.txt', 'r') as f:
    transmissions = [line.strip() for line in f.readlines()]

# Define the possible roof choices
roofs = ['Sunroof', 'Moonroof', 'Noroof']


# Define the start and goal states
start_state = ('EFI', 'Danlop', 'AT', 'Noroof')
goal_state = ('V12', 'Pirelli', 'CVT', 'Sunroof')
#goal_state = ('EFI', 'Danlop', 'CVT', 'Noroof')


# Define the probability function for simulated annealing
def prob(delta_e, temp):

    if delta_e < 0:                                  # checking if proposed state is better or not.
        return 1.0                                   # if better return 1 which means accept the state
    # calculates the probability according to the Boltzmann distribution.
    # The larger the delta_e, the smaller the probability of accepting the proposed state.
    return pow(2.71828, -delta_e / temp)


# Define a function to generate a random neighbor of the given state
def get_neighbor(state):

    while True:
        engine = random.choice(engines)                     # randomly chosen engine from engines
        tire = random.choice(tires)                         # randomly chosen tire from tires
        transmission = random.choice(transmissions)         # randomly chosen transmission from transmissions
        roof = random.choice(roofs)                         # randomly chosen roof from roofs
        neighbor = (engine, tire, transmission, roof)       # state of randomly chosen components

        if neighbor != state and neighbor in valid_cars:
            return neighbor                                 # generating the state which is valid & not equal to it's parent


# Define a function to calculate the cost (i.e., number of mismatched components) between two states
def cost(state1, state2):
    return sum(c1 != c2 for c1, c2 in zip(state1, state2))


# Define the simulated annealing algorithm to find the shortest path from start_state to goal_state
def simulated_annealing(start_state, goal_state):
    # initializing the start , goal , staring cost & temperature for simulated annealing
    current_state = start_state
    current_cost = cost(start_state, goal_state)
    best_state = start_state
    best_cost = current_cost
    temp = 1.0

    # exploring states & calculating delta_e for accepting the state
    while current_state != goal_state:
        neighbor = get_neighbor(current_state)
        neighbor_cost = cost(neighbor, goal_state)
        delta_e = neighbor_cost - current_cost

        # delta_e <= 0 means accepting the better states
        # random.uniform(0, 1) <= prob(delta_e, temp) means based on probability accepting the worse state
        if delta_e <= 0 or random.uniform(0, 1) <= prob(delta_e, temp):
            current_state = neighbor
            current_cost = neighbor_cost

        # calculation for years required
        if current_cost < best_cost:
            best_state = current_state          # updating the best_cost if found minimum than best_cost
            best_cost = current_cost
        temp = 1.0 / len(str(best_cost))

    return best_state


# Check if the goal state is a valid state
if goal_state not in valid_cars:
    print("Goal state is not a valid state")
else:
    # Run the simulated annealing algorithm and print the result
    result = simulated_annealing(start_state, goal_state)

    print(f"Start state: {start_state}")
    print(f"Goal state: {goal_state}")

    # printing the minimum years to reach the dream car or goal state
    if result is not None:
        print(f"Minimum needed to reach the goal state : {cost(start_state, result)} years")


