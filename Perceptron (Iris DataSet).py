# Use pip3 install numpy in the terminal
# Use pip3 install pandas in the terminal
# Use pip3 install matplotlib in the terminal

# Import essential libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Download the Iris dataset directly from UCI Machine Learning Repository
url = '/Users/shivesh/Desktop/PythonProject/Python Machine Learning Textbook/Chapter 2/Perceptron (Iris DataSet)/iris.data.csv'

# Read the CSV into a pandas DataFrame
df = pd.read_csv( url , header=None, encoding='utf-8')

# Show the last 5 rows to confirm successful load
print(df.tail())

# Select only the first 100 rows (Iris-setosa and Iris-versicolor)
y = df.iloc[0:100, 4].values   # Species column
# Convert class labels to integers: setosa = -1, versicolor = 1
y = np.where(y == 'Iris-setosa', -1, 1)

# Select two features: sepal length (0) and petal length (2)
X = df.iloc[0:100, [0, 2]].values

# Create a scatter plot: red for setosa, blue for versicolor
plt.scatter(X[:50, 0], X[:50, 1], color='red', marker='o', label='setosa')
plt.scatter(X[50:100, 0], X[50:100, 1], color='blue', marker='x', label='versicolor')

plt.xlabel('Sepal length [cm]')
plt.ylabel('Petal length [cm]')
plt.legend(loc='upper left')
plt.show()

class Perceptron(object):
    """
    Perceptron classifier.

    Parameters
    ----------
    eta : float
        Learning rate (between 0.0 and 1.0)
    n_iter : int
        Passes over the training dataset (epochs)

    Attributes
    ----------
    w_ : 1d-array
        Weights after fitting
    errors_ : list
        Number of misclassifications (updates) in each epoch
    """
    def __init__(self, eta=0.01, n_iter=10):
        self.eta = eta
        self.n_iter = n_iter

    def fit(self, X, y):
        """Fit training data."""
        self.w_ = np.zeros(1 + X.shape[1])  # Initialize weights (including bias)
        self.errors_ = []

        for _ in range(self.n_iter):
            errors = 0
            for xi, target in zip(X, y):
                # Calculate the update value (learning rule)
                update = self.eta * (target - self.predict(xi))
                # Update the weights (skip index 0, which is the bias)
                self.w_[1:] += update * xi
                self.w_[0] += update   # bias
                # Count updates
                errors += int(update != 0.0)
            self.errors_.append(errors)
        return self

    def net_input(self, X):
        """Calculate net input (weighted sum plus bias)"""
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def predict(self, X):
        """Return class label after unit step"""
        return np.where(self.net_input(X) >= 0.0, 1, -1)

# Create perceptron object, set learning rate and number of epochs
ppn = Perceptron(eta=0.1, n_iter=10)

# Train the model
ppn.fit(X, y)

# Plot misclassifications (errors) per epoch
plt.plot(range(1, len(ppn.errors_) + 1), ppn.errors_, marker='o')
plt.xlabel('Epochs')
plt.ylabel('Number of misclassifications')
plt.show()

from matplotlib.colors import ListedColormap

def plot_decision_regions(X, y, classifier, resolution=0.02):
    # Setup marker generator and color map
    markers = ('s', 'x')
    colors = ('lightgreen', 'gray')
    cmap = ListedColormap(colors[:len(np.unique(y))])

    # Plot the decision surface
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                           np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.3, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    # Plot class samples
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1],
                    alpha=0.8, c=colors[idx],
                    marker=markers[idx], label=cl)

# Now, use this function to plot decision regions
plot_decision_regions(X, y, classifier=ppn)
plt.xlabel('Sepal length [cm]')
plt.ylabel('Petal length [cm]')
plt.legend(loc='upper left')
plt.show()

