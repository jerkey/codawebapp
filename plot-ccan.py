from interpretcan import interpretCandumpTALine, can_db
import sys
import numpy as np

use_can_db = can_db('CODA-C-CAN-cells.dbc')

plotdata = np.ndarray((0,104),int)  # init an array of arrays of 104 integers

with open(sys.argv[1], "r") as logfile: # (2026-09-17 02:18:52.275524)  can1  005   [8]  0C E7 0C E9 0C E8 0C E4
    celldata = {}
    for line in logfile:
        timestamp = line[2:27]
        linedata = interpretCandumpTALine(line.strip(),use_can_db.db)
        try:
            celldata.update(linedata)
        except:
            print('linedata ' + str(linedata))
            pass
        if len(celldata) == 104:
            print('\n\r'+timestamp, end=' ')
            cellvoltages = list(range(104)) # init array of numbers
            for i in range(104):
                cellvoltages[i] = celldata['Cell'+str(i+1)]
                print(cellvoltages[i], end=',')
            celldata = {} # reset counter
            if max(cellvoltages) < 4000:    # sometimes we get 65535's
                plotdata = np.vstack([plotdata, cellvoltages])    # append this set of cellvoltages

import matplotlib.pyplot as plt

x = np.arange(len(plotdata))    # make an x axis
#print('len(plotdata) = ' + str(len(plotdata)))
print('plotdata.shape = ' + str(plotdata.shape))
nx, ny = plotdata.shape
x = np.arange(nx)
y = np.arange(ny)
X, Y = np.meshgrid(x, y, indexing='ij')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(X, Y, plotdata, cmap='coolwarm')    # see how matplotlib for more colors

ax.set_xlabel('t')
ax.set_ylabel('Cell')
ax.set_zlabel('mV')
ax.set_yticks(list(range(104)))
ax.set_yticklabels(list(range(104)), fontsize=10)
ax.set_box_aspect((1, 1, 1), zoom=1.5)  # 2x zoomed in
#ax.set_ylim(45, 65) # only show cells 45 to 65
plt.show()
