"""
1482 Elements (Number of scans)
478 rows (Number of unique rooms)
"""

import json
import os

from extract_json import *

def write_scans(all_scans):
    print(all_scans)

    with open('../../Downloads/55f5e35992ea91157b789b15eac4d432-a138ebba410f90c478ae4756b1b32912414ea0e4 3/rooms.txt', 'w+') as f:
        f.write("Reference Room" + " "*23 + "Scans-->"+ '\n')

        for i, room_scans in enumerate(all_scans):
            for scan in room_scans:
                f.write("%s%s" % (scan, ' '))
            f.write('\n')

def extract_single_room(room):
    # type(room) -->  dict
    PRINT_TESTS = False

    #printing test
    if PRINT_TESTS:
        print(room)
        print(room['reference'])
        print(room["scans"])

    #initialize variable names
    room_id = room['reference'] #id for the room; 1/478 unique room

    #list of all scan ids
    if room_id in excludes:
        scan_ids = []
    else:
        scan_ids = [room_id]

    #scans = room["scans"]
    num_scans = len(room["scans"])
    scan = room["scans"]

    for i in range (num_scans):
        scan_id = scan[i]['reference']
        if scan_id in excludes:
            pass
        else:
            scan_ids.append(scan_id)
    all_scans.append(scan_ids)
    #rint(scan_ids)

if __name__ == "__main__":

    all_scans = [] #with all scans, organized by which room it belongs to; length = num of unique rooms
    data = load_json("3RScan.json")
    #excludes = ["9766cbfb-6321-2e2f-806d-4bc43ad22fa4"]
    excludes = []

    #load all scans
    for room_i in range (len(data)):
        extract_single_room(data[room_i])

    write_scans(all_scans)

