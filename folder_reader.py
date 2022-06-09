import os
import json
PRINT_ALL_JSON = False

#load entire json file for raw data
def load_json(name):
    with open(name) as f:
      data = json.load(f)
    return data

#helper functions
def extract_centroid(data):
    return data["centroid"]

def printing_format(id, centroid, lable):
    print("===================================")
    print("Object ID: {}".format(id))
    print("Centoid Info: x: {}, y: {}, z: {}".format(centroid[0],centroid[1],centroid[2]))
    print("Label: {}".format(lable))

def write_object_info(name, id, centroid, lable):
    #file_name = "all_objects/"+name + "_object.txt"
    file_name = "no_sequence/" +name +"/" + name+ "_object.txt"

    #Format Object ID, Centoids, Label
    #print("the name: "+ file_name)
    with open (file_name, "a+") as f:
        f.write(str(id) + ",")
        f.write(str(centroid[0]) +  "," + str(centroid[1]) +  "," + str(centroid[2]) +  ",")
        f.write(lable)
        f.write("\n")
        # f.write("===================================\n")
        # f.write("Object ID: {}".format(id))
        # f.write("\n")
        # f.write("Centoid Info: x: {}, y: {}, z: {}".format(centroid[0],centroid[1],centroid[2]))
        # f.write("\n")
        # f.write("Label: {}".format(lable))
        # f.write("\n")

#extract objectID, label and centroid
def extract_segGroup_info(name, data):

    id_dict = {}
    label_dict = {}

    #loop through all segGroup objects
    for object_dict in data["segGroups"]:
        #object_dict includes: objectId, id, partId, index, dominantNormal, obb, segments, label

        #get needed info
        id = object_dict["objectId"]
        centroid = extract_centroid(object_dict["obb"])
        lable = object_dict["label"]

        #print
        #printing_format(id,centroid,lable)
        write_object_info(name, id,centroid,lable)
        id_dict[id] = [lable, centroid]

        if lable in label_dict:
            label_dict[lable].append([id, centroid])
        else:
            label_dict[lable] = [[id, centroid]]
        #print("object id is: {}, the centroid is: {} and the label is: {}".format(id,centroid,lable))

    return id_dict, label_dict

def remove_intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]

    for i in lst3:
        lst1.remove(i)
    return lst1

def read_folder():
    folder_name = "no_sequence"
    #sub_folder = "no_sequence/0a4b8ef6-a83a-21f2-8672-dce34dd0d7ca"
    folders = os.listdir(folder_name)
    excludes = []

    folders = remove_intersection(folders, excludes)

    #loop through all folders
    for i in range (len(folders)):
        room_id = folders[i]
        if room_id == ".DS_Store":
            pass
        else:
            room_semseg = "no_sequence/"+ room_id + "/semseg.v2.json"
            #print(room_semseg)

            get_object_info(room_id, room_semseg)



def get_object_info(name, path):

    try:
        data = load_json(path)
        # printing only object ID, centoid and label
        id_dict, label_dict = extract_segGroup_info(name, data)

        # dictionary organized by id, and dictionary organized by label
        # print(id_dict)
        # print(label_dict)

    except FileNotFoundError:
        #print("no semseg file found in: "+ name)
        no_semseg.append(name)

def excluded_files(list):
    with open('excluded.txt', 'w+') as f:
        for i in list:
            f.write('%s\n' % i)


if __name__ == "__main__":
    no_semseg = []
    read_folder()
    excluded_files(no_semseg)
