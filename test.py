import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Create a simple scatter plot
x_values = [1, 2, 3, 4, 5]
y_values = [2, 3, 5, 7, 11]
plt.scatter(x_values, y_values, label='Scatter Plot')

# Define the coordinates for the Line2D
line_x = [1, 5]
line_y = [2, 11]

# Create a Line2D object
line = Line2D([0], [0], color='red', linewidth=2, linestyle='dashed', label='Line2D')

# Set labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Line2D at Specific Coordinates')

# Add a legend
legend = plt.legend([line], ['Hello'])

# Show the plot
plt.show()
