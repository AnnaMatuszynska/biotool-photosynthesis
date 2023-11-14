# To get the same design as us
text_color = "#727682"

with plt.rc_context(
    {
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.edgecolor": text_color,
        "font.size": 12.0,
        "text.color": text_color,
        "axes.labelcolor": text_color,
        "xtick.color": text_color,
        "ytick.color": text_color,
        "grid.color": text_color,
        "font.weight": 'bold',
        "axes.prop_cycle": cycler(color=["#f9a51b", "#d1232a", "#1062ef"])  
    }
):
    fig, ax = plt.subplots(figsize = (7, 4))

    for i in ['S', 'I', 'R']:
        ax.plot(
            res['t'],
            res['y'][['S', 'I', 'R'].index(i)],
            label = i,
            linestyle = 'solid',
            linewidth = 5
        )

# Set Axis titles
plt.xlabel('Time [Months]', fontsize = 12, weight= 'bold')
plt.ylabel('Population size [a.u.]', fontsize = 12, weight= 'bold')

# Change the left and down limit
plt.xlim(0)
plt.ylim(0)

# Create and center legend
plt.legend(loc = 'center right', frameon = False, labelcolor = 'linecolor', fontsize = 12, prop = {'weight':'bold'})

plt.tight_layout()

# Show the plot
plt.show()

# Uncomment to save the figure
#plt.savefig('./pictures/SIR_manual.png', transparent = True, edgecolor = 'white')
