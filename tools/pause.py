#! /usr/bin/python3
# Purpose: sum up total GC pause time from a Shenandoah GC log file
# Attention: !!!Only tested with default Cassandra GC log options!!!
# Usage: python3 .../pause.py <log_file_path>
# e.g. /mnt/ssd/shiliu/cassandra/tools/pause.py /mnt/ssd/shiliu/cassandra/logs/13-UInsert.log
# Last modified: 11/02/2021

import sys

file = sys.argv[1]

if __name__ == '__main__':
    pause_time = []
    lines = open(file).readlines()
    for line in lines:
        line_after_timestamp = line.split("]")[-1]
        splitted = line_after_timestamp.split()

        if (len(splitted) < 2):
          continue

        if splitted[1].startswith("Pause"):  
            cur_pause_time = splitted[-1][0:-2] # e.g. get the time,  splitted[-1]:27.633ms -> 27.633
            pause_time.append(float(cur_pause_time)/1000)
    pause_sum = sum(pause_time)
    print('Total pause time: ' + "{:5.3f}".format(pause_sum) + ' seconds')

