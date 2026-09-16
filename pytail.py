import time
import os
import sys
from pathlib import Path    # for finding newest logfiles

log_directory = Path(sys.argv[1])
newest_file_BCAN = max(log_directory.glob('can0*.log'), key=lambda f: f.stat().st_ctime) # Find newest file by creation time
newest_file_CCAN = max(log_directory.glob('can1*.log'), key=lambda f: f.stat().st_ctime) # Find newest file by creation time
print('BCAN	'+str(newest_file_BCAN))
print('CCAN	'+str(newest_file_CCAN))

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
with open(newest_file_CCAN, "r") as logfile:
    for line in follow(logfile):
        print(line.strip())   
