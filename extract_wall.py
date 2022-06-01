from os import remove


def extract_wall_txt(input_path, output_path):
    """
    Extract walls from input ply, remove other data points.
    """
    with open(input_path, 'r') as plyfile:
        full_ply_list = plyfile.readlines()
    plyfile.close()
    element_face_line = None
    element_face_line_is_found = False
    i = 0
    removed_face_counter = 0
    remove_list = []
    remove_vertex_index_list = []
    removed_vertex_counter = 0
    for k in range(100000):
        remove_vertex_index_list.append([])
    vertex_line_is_found = False
    vertex_line_num = None
    face_line_is_found = False
    face_line_num = None
    element_vertex_line = None
    element_vertex_line_is_found = False
    # detect all irrelevant rows
    for row in full_ply_list:
        row_list = row.split()
        # find element face line
        if element_vertex_line_is_found == False:
            if (row_list[0] == 'element') and (row_list[1]=='vertex'):
                element_vertex_line = i
                element_vertex_line_is_found = True
        elif element_face_line_is_found == False:
            if (row_list[0] == 'element') and (row_list[1]=='face'):
                element_face_line = i
                element_face_line_is_found = True
        elif (len(row_list) == 11):
            if not vertex_line_is_found:
                vertex_line_num = i
                vertex_line_is_found = True
            relevant_list = [503, 504, 505, 506, 507, 188, 189]
            if (int(row_list[7]) not in relevant_list):
            #if (int(row_list[7]) < 503) or (int(row_list[7]) > 507):
                remove_list.append(i)
                removed_vertex_counter += 1
                remove_vertex_index_list[(i-vertex_line_num)%100000].append(i-vertex_line_num)
        # detect all faces that should be removed
        elif (len(row_list) == 4 and (int(row_list[0])==3)):
            for vertex_index in row_list:
                if not face_line_is_found:
                    face_line_num = i
                    face_line_is_found = True
                if (int(vertex_index) in remove_vertex_index_list[(int(vertex_index))%100000]):
                    remove_list.append(i)
                    removed_face_counter += 1
                    break
        i += 1
        if (i%10000==0):
            print(i)
    # Change the element vertex line
    old_element_num = int(full_ply_list[element_vertex_line].split()[2])
    new_num = old_element_num-removed_vertex_counter
    new_str = 'element vertex ' + str(new_num) + '\n'
    print(element_vertex_line)
    full_ply_list.remove(full_ply_list[element_vertex_line])
    full_ply_list.insert(element_vertex_line, new_str)
    # Change the element face line
    old_face_num = int(full_ply_list[element_face_line].split()[2])
    new_num = old_face_num-removed_face_counter
    new_str = 'element face ' + str(new_num) + '\n'
    print(element_face_line)
    full_ply_list.remove(full_ply_list[element_face_line])
    full_ply_list.insert(element_face_line, new_str)
    # pair the wall datapoints' old row number with new row number
    l = 0
    index_pair_list = []
    for i in range(face_line_num-vertex_line_num):
        index_pair_list.append(-1)
    for m in range(face_line_num-vertex_line_num):
        if ((m+vertex_line_num)==remove_list[l]):
            l += 1
        else:
            index_pair_list[m] = (m-l)
    #print(index_pair_list)
    # detele rows
    j = 0
    for index in remove_list:
        full_ply_list.remove(full_ply_list[index-j])
        j += 1
    # change the value in face data
    row_index = 0
    for row in full_ply_list:
        row_list = row.split()
        if (len(row_list) == 4 and (int(row_list[0])==3)):
            new_vertex_index = []
            vertex_index_column = 0
            for vertex_index in row_list:
                if vertex_index_column == 0:
                    new_vertex_index.append(vertex_index)
                else:
                    new_vertex_index.append(str(index_pair_list[int(vertex_index)]))
                vertex_index_column += 1
            row_str = ''
            
            for vertex_index in new_vertex_index:
                row_str += (' ' + vertex_index)
            row_str += '\n'
            full_ply_list.remove(row)
            full_ply_list.insert(row_index, row_str)
        row_index += 1
    # write the new list to output file
    with open(output_path, 'w') as outputfile:
        outputfile.writelines(full_ply_list)
    outputfile.close()


if __name__ == '__main__':
    input_path = '/home/lin/Documents/Others/ExtractWall/labels.instances.annotated.v2.ply'
    output_path = '/home/lin/Documents/Others/ExtractWall/wall.ply'
    extract_wall_txt(input_path, output_path)
