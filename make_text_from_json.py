import os
import sys
import string
import json

file_path = sys.argv[1]
output_file_path = sys.argv[2]

print("loading....")
with open(file_path, 'rb') as data_file:
    data = json.load(data_file)

print("dumping....")

if not os.path.exists(os.path.dirname(output_file_path)):
    os.makedirs(os.path.dirname(output_file_path))

list_of_keys = [obj.keys()[0] for obj in data]
with open(output_file_path, 'w') as f:
    # json.dump(data[998], f)
    for item in list_of_keys:
        f.write("%s\n" % item)

# read_from_file()

# with open(file_path, 'rb') as f:
#     f_content = f.readlines()
    
#     for keyword in f_content :
#         keyword = keyword.strip()
        
# file_iterator+=1
