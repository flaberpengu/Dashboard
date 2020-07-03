import psutil
import matplotlib.pyplot as plt
import numpy as np

##Colours used for bars on graph
colours = ['red', 'blue', 'green']

##Get the values to plot
yVals = np.arange(1,9)
xVals = psutil.cpu_percent(interval=5, percpu=True)

##Plot a horizontal bar chart
plt.barh(yVals, xVals, align='center', alpha=0.75, zorder=100, color=colours)
plt.ylabel("CPU Cores")
plt.xlabel("% Usage")
plt.grid(zorder=0)

##Save the graph
plt.savefig('processor_info_percpu_usage.png', bbox_inches='tight', dpi=300)
#plt.show()
