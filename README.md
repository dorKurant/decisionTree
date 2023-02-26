Implementation of a decision tree in Python without using ready-made packages.
This algorithm uses data from the Korean National Health Insurance to predict whether a person is a smoker based on various health indicators.

Broadly, the last variable indicates whether a person is a smoker or not. The other variables represent different health measurements of the person.
Some of these variables are continuous, so I set thresholds to categorize them into buckets.
For each attribute, I sorted the data from smallest to largest and split them into three buckets of equal size. 
When building my decision trees, I use entropy to calculate the most meaningful attributes and χ2 test to prune vertices.

Here's an explanation of the functions:
build_tree(ratio) - This function builds a decision tree using a specified ratio of the data for training and the remaining data for validation.
The ratio parameter is a float value between 0 and 1, representing the percentage of data to be used for training.
The function prints out the decision tree and reports the error.

tree_error(k) - This function evaluates the quality of the decision tree by performing k-fold cross-validation,where k is an integer number of folds.
The function reports the average error rate of the k trees that are built.
For example, if k is 6, the function builds 6 different trees and returns their average error rate.

is_busy(row_input) - This function takes an array of values as input for a particular person,
in the same order as the data file but without the smoker column.
The function returns 1 if it thinks the person is a smoker and 0 if not. The decision tree is built using the full data.
