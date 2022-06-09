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

def write_object_info(id, centroid, lable):
    with open ("../../Downloads/55f5e35992ea91157b789b15eac4d432-a138ebba410f90c478ae4756b1b32912414ea0e4 3/object.txt", "a+") as f:
        f.write("===================================\n")
        f.write("Object ID: {}".format(id))
        f.write("\n")
        f.write("Centoid Info: x: {}, y: {}, z: {}".format(centroid[0],centroid[1],centroid[2]))
        f.write("\n")
        f.write("Label: {}".format(lable))
        f.write("\n")

#extract objectID, label and centroid
def extract_segGroup_info(data):

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
        printing_format(id,centroid,lable)
        write_object_info(id,centroid,lable)
        id_dict[id] = [lable, centroid]

        if lable in label_dict:
            label_dict[lable].append([id, centroid])
        else:
            label_dict[lable] = [[id, centroid]]
        #print("object id is: {}, the centroid is: {} and the label is: {}".format(id,centroid,lable))

    return id_dict, label_dict


if __name__ == "__main__":
    file_name = '../../Downloads/55f5e35992ea91157b789b15eac4d432-a138ebba410f90c478ae4756b1b32912414ea0e4 3/no_sequence/0a4b8ef6-a83a-21f2-8672-dce34dd0d7ca/semseg.v2.json'
    data = load_json(file_name)

    #to print all json info
    if PRINT_ALL_JSON:
        print(data)

    #printing only object ID, centoid and label
    id_dict, label_dict = extract_segGroup_info(data)

    #dictionary organized by id, and dictionary organized by label
    print(id_dict)
    print(label_dict)