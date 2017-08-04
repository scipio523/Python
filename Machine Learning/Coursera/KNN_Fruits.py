# train knn classifier to classify fruits
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# load data
fruits = pd.read_table('fruit_data_with_colors.txt')
X = fruits[['mass', 'width', 'height']]
y = fruits['fruit_label']

# divide data into train/test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

# fit knn classifier
knn = KNeighborsClassifier(n_neighbors = 5)
knn.fit(X_train, y_train)

# see how accurate model is on test data
print knn.score(X_test, y_test)

# predict additional examples
lookup_fruit_name = dict(zip(fruits.fruit_label.unique(), fruits.fruit_name.unique()))
example_fruit = [[20, 4.3, 5.5]]
fruit_prediction = knn.predict(example_fruit)
print lookup_fruit_name[fruit_prediction[0]]




