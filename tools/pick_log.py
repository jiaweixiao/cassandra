#! /usr/bin/python3
"""
Purpose: extract log messages of a specific time period from a Cassandra log file
Usage: python3 .../pick_log.py <log_file_path> <extracted_log_file_path> <start_time> <end_time>
e.g. ${HOME}/cassandra/tools/pick_log.py ${HOME}/cassandra/logs/IIUInsert-13-gc.log ${HOME}/cassandra/logs/13-UInsert.log 2021-11-01T20:01:50 2021-11-01T21:07:05
Last modified: 11/08/2021
"""

import sys
import datetime

raw_log = sys.argv[1]
extracted_log = sys.argv[2]

# start and end time format: YYYY-MM-DDTHH:MM:SS
# e.g. 2021-11-01T17:54:59

s = sys.argv[3]
e = sys.argv[4]

if __name__ == '__main__':
    pause_time = []
    start_time = datetime.datetime(int(s[0:4]), int(s[5:7]), int(s[8:10]), int(s[11:13]), int(s[14:16]), int(s[17:19]))
    end_time = datetime.datetime(int(e[0:4]), int(e[5:7]), int(e[8:10]), int(e[11:13]), int(e[14:16]), int(e[17:19]))
    lines = open(raw_log).readlines()
    with open(extracted_log, 'a', encoding='utf-8') as f:
        extraction_start = False
        for line in lines:
            t = line.split("]")[0][1:20]
            cur_time = datetime.datetime(int(t[0:4]), int(t[5:7]), int(t[8:10]), int(t[11:13]), int(t[14:16]), int(t[17:19]))
            if not extraction_start:
                if cur_time >= start_time:
                    extraction_start = True
                    f.write(line)
            else:
                if cur_time <= end_time:
                    f.write(line)
                else:
                    break
    print("Done!")
