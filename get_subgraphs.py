import os
import sys
import string
import operator
import numpy as np
walk_dir = sys.argv[1]
output_dir = sys.argv[2]

print('walk_dir = ' + walk_dir)

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
        if os.path.isdir(os.path.join(a_dir, name))]

subdirs = get_immediate_subdirectories(walk_dir)

submatrix_size=200

for walk_subdir in subdirs:
    absolute_path = os.path.join(walk_dir, walk_subdir)

    for root, subdirs, files in os.walk(absolute_path):
        print("changing folder"+root)
        for filename in files:
            file_path = os.path.join(root, filename)

            with open(file_path, 'rb') as data_file:    
                data = np.load(data_file)

            data = data[0:submatrix_size, 0:submatrix_size]         

            output_usr_dir = os.path.join(output_dir, walk_subdir)
            output_file_path = output_usr_dir+'/'+filename
            if not os.path.exists(os.path.dirname(output_file_path)):
                os.makedirs(os.path.dirname(output_file_path))
            # op = open(output_file_path, 'w')
            # np.save(op, arr)
            np.savetxt(output_file_path, data)
