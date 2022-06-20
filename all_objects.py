import os
import json
import csv
import collections
from itertools import dropwhile
import pandas as pd

#read all the scan names for all the rooms
def read_folder_names(folder_name):
    #sub_folder = "no_sequence/0a4b8ef6-a83a-21f2-8672-dce34dd0d7ca"
    folders = os.listdir(folder_name)
    return folders

#read each scan's object data info
def read_folder_content(file_name):
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    #print(data)
    return data

#extract id and object name from given scan data
def extract_all_objects(data):
    for object in data:
        object_id = object[0]
        object_name = object[-1]
        occurances_list.append(object_name)
        all_objects.add(object_name)

def write_to_txt(f_name, list):
    with open(f_name, 'w') as f:
        for item in list:
            f.write("%s\n" % item)

#filter out dict key if value < min
def filter_occurances(all_objects, min):
    for key, count in dropwhile(lambda key_count: key_count[1] >= min, all_objects.most_common()):
        del all_objects[key]

    return all_objects

#Go through all scans and extract object info, update all_objects
def create_all_objects_txt():
    for f_name in folder_names:
        full_address = "all_objects_v2/" + f_name
        room_content = read_folder_content(full_address)
        extract_all_objects(room_content)
    #print(all_objects)

    #write all_objects
    write_to_txt("all_object.txt", all_objects)


def occurance_txt(f_name, dict):
    with open(f_name, 'w') as f:
        for key, value in dict.items():
            f.write('%s,%s\n' % (key, value))


def create_frequent_objects_txt():
    # Find occurances of all_objects and store in dict
    occurrences = collections.Counter(occurances_list)
    print(occurrences)

    # filter out less frequent objects
    frquent_occurrences = filter_occurances(occurrences, 50)
    print(frquent_occurrences)
    occurance_txt("objects_and_frequency.txt", frquent_occurrences)
    write_to_txt("frequent_object.txt", frquent_occurrences)

def read_excel():
    file_name = r'3RScan.v2 Semantic Classes.xlsx'
    #df = pd.read_excel(file_name)
    df = pd.read_excel(file_name, sheet_name='Mapping', usecols="B")
    #print(df)
    labels = df.values.reshape(-1, ).tolist()
    return labels

if __name__ == "__main__":
    all_objects = set()
    occurances_list = []
    folder_names = read_folder_names("all_objects_v2")
    new_id_frequent_objects = []

    create_all_objects_txt()
    create_frequent_objects_txt()


    #match ids
    excel_ids = read_excel()
    #temp_set = ()

    for object in occurances_list:
        #temp_set.add(object)
        new_id = excel_ids.index(object)
        new_id_frequent_objects.append(object + "," + str(new_id))

    #write_to_txt("new_id_frequent_objects.txt", new_id_frequent_objects)
    #print(new_id_frequent_objects)


    #meta file: object:frequency


