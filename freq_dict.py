import os
import sys
import string
import json
import operator

walk_dir = sys.argv[1]
output_dir = sys.argv[2]


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
        if os.path.isdir(os.path.join(a_dir, name))]

print('walk_dir = ' + walk_dir)

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

# Create dict<> of keyword and it's document list
# [
#   {"heather": {
#       "doc": {
#           "/home/alok/Projects/security/key_simple/1.": 2
#       },
#       "freq": 2
#      }
#   },
#   {"ani": {
#       "doc": {
#           "/home/alok/Projects/security/key_simple/1.": 1
#       },
#       "freq": 1
#       }
#   },
#   {"aani": {
#       "doc": {
#           "/home/alok/Projects/security/key_simple/1.": 1
#       },
#       "freq": 1
#       }
#    }
# ]

def write_to_file(dict_obj, output_dir):
    print("dumping.....")

    global op_file_name
    global func_call_counter

    output_file_path = output_dir+op_file_name+str(func_call_counter)+'.json'
    if not os.path.exists(os.path.dirname(output_file_path)):
        os.makedirs(os.path.dirname(output_file_path))
    with open(output_file_path, 'w') as f:
        json.dump(dict_obj, f)
    func_call_counter+=1

op_file_name = '/freq_dict-'


subdirs = get_immediate_subdirectories(walk_dir)

for walk_subdir in subdirs:
    absolute_path = os.path.join(walk_dir, walk_subdir)
    print(absolute_path)
    count = 0
    dict_obj = {}
    file_iterator=0
    for root, subdirs, files in os.walk(absolute_path):
        # print("changing folder"+root)

        for filename in files:
            count+=1
            if count%50000 == 0 :
                print ("Done %d objects" %(count))

            # file_path = os.path.join(root, filename)

            # with open(file_path, 'rb') as f:
            #     f_content = f.readlines()
                
            #     for keyword in f_content :
            #         keyword = keyword.strip()
            #         if keyword in dict_obj :
            #             dict_obj[keyword]['tf'] += 1
            #             if file_iterator in dict_obj[keyword]['did'] :
            #                 dict_obj[keyword]['did'][file_iterator] += 1
            #             else :
            #                 dict_obj[keyword]['did'][file_iterator] = 1
            #                 dict_obj[keyword]['df'] += 1
            #         else :
            #             dict_obj[keyword] = {}
            #             dict_obj[keyword]['df'] = 1
            #             dict_obj[keyword]['tf'] = 1
            #             dict_obj[keyword]['did'] = {}
            #             dict_obj[keyword]['did'][file_iterator] = 1
            file_iterator+=1

    # for i in dict_obj:
    #     dict_obj[i].pop('did', None)

    print("sorting.....")
    # dict_obj = list(dict_obj.iteritems())
    # dict_obj.sort(key=lambda x:x[1]["df"], reverse=True)
    # dict_obj = [{x:y} for x,y in dict_obj]

    # for i in range(len(dict_obj)/1000 +1):
    output_usr_dir = os.path.join(output_dir, walk_subdir)
    # write_to_file(dict_obj[0:1000], output_usr_dir)
    func_call_counter = 1
    write_to_file([{'total_number_of_files':file_iterator}], output_usr_dir)
