from interpretcan import interpretCandumpTALine, can_db, can0_db, can1_db
import sys
#from pathlib import Path    # for finding newest logfiles

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

# Usage
use_can_db = can_db('CODA-C-CAN-cells.dbc')
use_can_db.add_dbc('CODA-D-CAN.dbc')
#exit(1)
with open(sys.argv[1], "r") as logfile:
    for line in logfile:
        print(interpretCandumpTALine(line.strip(),use_can_db.db) )
