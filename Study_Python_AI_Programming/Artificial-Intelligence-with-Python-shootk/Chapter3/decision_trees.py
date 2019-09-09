import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn import model_selection
from sklearn.tree import DecisionTreeClassifier

input_file = "Artificial-Intelligence-with-Python-shootk\Chapter3\data_decision_trees.txt"
data = np.loadtxt(input_file, delimiter=',')
X, y = data[:, :-1], data[:, -1]
