from interpretcan import interpretCandumpTALine, can_db
import sys
import numpy as np

def follow(thefile):
    """Generator function that yields new lines in a file."""
    # Seek to the end of the file
    thefile.seek(0, os.SEEK_END)

    while True:
        line = thefile.readline()
        if not line:
            # Sleep briefly if no new data is available
            time.sleep(0.1)
            continue
        yield line

cell_value_names = ['Cell1', 'Cell2', 'Cell3', 'Cell4', 'Cell5', 'Cell6', 'Cell7', 'Cell8', 'Cell9', 'Cell10', 'Cell11', 'Cell12', 'Cell13', 'Cell14', 'Cell15', 'Cell16', 'Cell17', 'Cell18', 'Cell19', 'Cell20', 'Cell21', 'Cell22', 'Cell23', 'Cell24', 'Cell25', 'Cell26', 'Cell27', 'Cell28', 'Cell29', 'Cell30', 'Cell31', 'Cell32', 'Cell33', 'Cell34', 'Cell35', 'Cell36', 'Cell37', 'Cell38', 'Cell39', 'Cell40', 'Cell41', 'Cell42', 'Cell43', 'Cell44', 'Cell45', 'Cell46', 'Cell47', 'Cell48', 'Cell49', 'Cell50', 'Cell51', 'Cell52', 'Cell53', 'Cell54', 'Cell55', 'Cell56', 'Cell57', 'Cell58', 'Cell59', 'Cell60', 'Cell61', 'Cell62', 'Cell63', 'Cell64', 'Cell65', 'Cell66', 'Cell67', 'Cell68', 'Cell69', 'Cell70', 'Cell71', 'Cell72', 'Cell73', 'Cell74', 'Cell75', 'Cell76', 'Cell77', 'Cell78', 'Cell79', 'Cell80', 'Cell81', 'Cell82', 'Cell83', 'Cell84', 'Cell85', 'Cell86', 'Cell87', 'Cell88', 'Cell89', 'Cell90', 'Cell91', 'Cell92', 'Cell93', 'Cell94', 'Cell95', 'Cell96', 'Cell97', 'Cell98', 'Cell99', 'Cell100', 'Cell101', 'Cell102', 'Cell103', 'Cell104']

use_can_db = can_db('CODA-C-CAN-cells.dbc')
#exit(1)
# (2026-09-17 02:18:52.275524)  can1  005   [8]  0C E7 0C E9 0C E8 0C E4

plotdata = np.ndarray((0,104),int)  # init an array of arrays of 104 integers

with open(sys.argv[1], "r") as logfile:
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

#data = np.random.rand(100, 500)    # data shape: (100, N_points)
#x = np.arange(500)  # make an axis?
x = np.arange(len(plotdata))    # make an x axis
#print('len(plotdata) = ' + str(len(plotdata)))
print('plotdata.shape = ' + str(plotdata.shape))
nx, ny = plotdata.shape
x = np.arange(nx)
y = np.arange(ny)
X, Y = np.meshgrid(x, y, indexing='ij')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(X, Y, plotdata, cmap='coolwarm')

ax.set_xlabel('t')
ax.set_ylabel('Cell')
ax.set_zlabel('mV')
ax.set_yticks(list(range(104)))
ax.set_yticklabels(list(range(104)), fontsize=10)
ax.set_box_aspect((1, 1, 1), zoom=1.5)  # 2x zoomed in
#ax.set_ylim(45, 65) # only show cells 45 to 65
plt.show()
