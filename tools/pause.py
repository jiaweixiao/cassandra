#! /usr/bin/python3
"""
Purpose: sum up total GC pause time from a Shenandoah GC log file
Attention: !!!Only tested with default Cassandra GC log options and -Xlog:gc*!!!
Usage: python3 .../pause.py <log_file_path>
e.g. ${HOME}/cassandra/tools/pause.py ${HOME}/cassandra/logs/13-UInsert.log
Last modified: 11/08/2021
"""

import sys

file = sys.argv[1]

if __name__ == '__main__':
    pause_time = []
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line_after_timestamp = line.split("]")[-1]
            splitted = line_after_timestamp.split()

            if len(splitted) < 2:
                continue

            if splitted[1].startswith("Pause") and splitted[-1].endswith("ms"):
                # get the time, e.g. 27.633ms -> 27.633
                cur_pause_time = splitted[-1][0:-2]
                pause_time.append(float(cur_pause_time)/1000)
    pause_sum = sum(pause_time)
    print(f'Total pause time: {pause_sum:5.3f} seconds')
