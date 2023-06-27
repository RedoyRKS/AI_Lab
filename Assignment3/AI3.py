# Importing Python Module & Functions
import math
import csv
import pandas as pd
import numpy as np

dataset_file = "Assignment3\dataset.csv"              # Variable that stores the path of dataset file
mark_records = []                           # Empty list used to store the records in the dataset

# Dictionaries to store the minimum and maximum marks for each assignment and exam in the dataset.
min_marks = {
    "Assignment-1": 100,
    "Assignment-2": 100,
    "Assignment-3": 100,
    "Assignment-4": 100,
    "Assignment-5": 100,
    "Final": 100,
    "Mid": 100,
}

# Dictionaries to store the maximum marks for each assignment and exam in the dataset.
max_marks = {
    "Assignment-1": -100,
    "Assignment-2": -100,
    "Assignment-3": -100,
    "Assignment-4": -100,
    "Assignment-5": -100,
    "Final": -100,
    "Mid": -100,
}

# Finding the minimum and maximum values for each column in the dataset
def load_min_max(df):

    for k in min_marks:
        min_marks[k] = min(df.loc[:, k])
        max_marks[k] = max(df.loc[:, k])

# Normalize the values in a row using the minimum and maximum values for each column
# Formula for Normalize: (x - x_min) / range
# range = max_marks - min_marks
def get_normalized_entry(row):

    result = []

    result.append((row[0] - min_marks["Assignment-1"]) / (max_marks["Assignment-1"] - min_marks["Assignment-1"]))
    result.append((row[1] - min_marks["Assignment-2"]) / (max_marks["Assignment-2"] - min_marks["Assignment-2"]))
    result.append((row[2] - min_marks["Assignment-3"]) / (max_marks["Assignment-3"] - min_marks["Assignment-3"]))
    result.append((row[3] - min_marks["Assignment-4"] )/ (max_marks["Assignment-4"] - min_marks["Assignment-4"]))
    result.append((row[4] - min_marks["Assignment-5"]) / (max_marks["Assignment-5"] - min_marks["Assignment-5"]))
    result.append((row[5] - min_marks["Final"]) / (max_marks["Final"] - min_marks["Final"]))
    result.append((row[6] - min_marks["Mid"]) / (max_marks["Mid"] - min_marks["Mid"]))

    return result

# Load the dataset and normalize the values
df = pd.read_csv(dataset_file)
load_min_max(df)

for row in range(len(df)):
    current_record = list(df.loc[row, :])
    current_record_updated = [current_record[0]]
    current_record_updated.extend(get_normalized_entry(current_record[1: len(current_record) - 1]))
    current_record_updated.append(current_record[-1])
    mark_records.append(current_record_updated)

# Split the dataset into training, validation, and testing sets
training = mark_records[: math.floor(len(mark_records)*0.8)]
validation = mark_records[math.floor(len(mark_records)*0.8): math.floor(len(mark_records)*0.8) + math.floor(len(mark_records)*0.1)]
testing = mark_records[math.floor(len(mark_records)*0.8) + math.floor(len(mark_records)*0.1):]

# Calculating Euclidean Distance
def euclidean_distance(row1, row2):
    if len(row1) != len(row2):
        return None
    ret_val= 0
    for idx, item in enumerate(row1):
        ret_val += (row1[idx] - row2[idx]) ** 2
    return math.sqrt(ret_val)

#  Calculates the percentage of correct predictions/Accuracy
def get_accuracy(true_output, predicted_output):
    correct = 0
    for idx, outcome in enumerate(true_output):
        if predicted_output[idx] == outcome:
            correct += 1
    return correct / len(true_output) * 100

# List to store predicted output
predicted_output = []

# No of neighbours
k = 3

for entry in validation:
    dist_vector = []
    for compare_entry in training:
        if entry != compare_entry:
            # Calculate the Euclidean distance between the validation entry and each training entry
            sample1 = entry[1: len(entry) - 1]
            sample2 = compare_entry[1: len(compare_entry) - 1]
            dist_vector.append((euclidean_distance(sample1, sample2), compare_entry[-1]))

    # Sort the list of tuples based on the first element (distance)
    dist_vector.sort(key=lambda x: x[0])

    # Get the k nearest neighbors and their classes
    neighbors = [x[1] for x in dist_vector[:k]]

    # Determine the majority class among the neighbors
    predicted_class = max(set(neighbors), key=neighbors.count)

    # Add the predicted class to the output list
    predicted_output.append(predicted_class)


true_output = [entry[-1] for entry in validation]

accuracy = get_accuracy(true_output, predicted_output)
print(f"Validation accuracy: {accuracy:.2f}%")

test = mark_records[math.floor(len(mark_records) * 0.9):]

predicted_output = []

for entry in test:
    dist_vector = []
    for compare_entry in training:
        # Calculate the Euclidean distance between the test entry and each training entry
        sample1 = entry[1: len(entry) - 1]
        sample2 = compare_entry[1: len(compare_entry) - 1]
        dist_vector.append((euclidean_distance(sample1, sample2), compare_entry[-1]))

    # Sort the list of tuples based on the first element (distance)
    dist_vector.sort(key=lambda x: x[0])

    # Get the k nearest neighbors and their classes
    neighbors = [x[1] for x in dist_vector[:k]]

    # Determine the majority class among the neighbors
    predicted_class = max(set(neighbors), key=neighbors.count)

    # Add the predicted class to the output list
    predicted_output.append(predicted_class)

true_output = [entry[-1] for entry in test]

accuracy = get_accuracy(true_output, predicted_output)
print(f"Test accuracy: {accuracy:.2f}%")

