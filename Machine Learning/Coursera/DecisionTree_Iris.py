# train decision tree to classify iris flowers
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

iris = load_iris()

X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target,
													random_state = 3)

dt = DecisionTreeClassifier(max_depth = 3).fit(X_train, y_train)
tree_predicted = dt.predict(X_test)
confusion = confusion_matrix(y_test, tree_predicted)

print 'Decision tree classifier (max_depth = 3)\n', confusion
print 'Accuracy of Decision Tree classifier on training set: {:.2f}'.format(dt.score(X_train, y_train))
print 'Accuracy of Decision Tree classifier on test set: {:.2f}'.format(dt.score(X_test, y_test))
print classification_report(y_test, tree_predicted, target_names = iris.target_names)

