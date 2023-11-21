import matplotlib.pyplot as plt

# Create a sample plot
fig, ax = plt.subplots()
line1, = ax.plot([1, 2, 3], label='Line 1')
line2, = ax.plot([3, 2, 1], label='Liaadsadsada 2')

# Add legend with two columns
legend = ax.legend(loc='upper left', bbox_to_anchor=(0, 1), ncols=2)

for handle in legend.legend_handles:
    print(handle.get_bbox().max)
    print(legend.get_texts())

# Get the legend frame width
legend_width = ax.get_legend().get_frame().get_width()

# Calculate the width of each column
column_width = legend_width / 2

print(f"The width of each legend column is: {column_width}")

plt.show()
