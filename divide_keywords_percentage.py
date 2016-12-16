import os
import sys
import string
from shutil import copyfile


walk_dir = sys.argv[1]
output_dir = sys.argv[2]

print('walk_dir = ' + walk_dir)

import random
def random_subset( iterator, K ):
    result = []
    N = 0

    for item in iterator:
        N += 1
        if len( result ) < K:
            result.append( item )
        else:
            s = int(random.random() * N)
            if s < K:
                result[ s ] = item

    return result

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

for root, subdirs, files in os.walk(walk_dir):
    file_count = len(files)
    keys = random_subset(files, file_count/2)
    tags = [item for item in files if item not in keys]

    for filename in keys:
        file_path = os.path.join(root, filename)        
        output_file_path = file_path.replace(walk_dir, output_dir+"keys"+'/')
        if not os.path.exists(os.path.dirname(output_file_path)):
            os.makedirs(os.path.dirname(output_file_path))
        copyfile(file_path, output_file_path)


    for filename in tags:
        file_path = os.path.join(root, filename)
        output_file_path = file_path.replace(walk_dir, output_dir+"tags"+'/')
        if not os.path.exists(os.path.dirname(output_file_path)):
            os.makedirs(os.path.dirname(output_file_path))
        copyfile(file_path, output_file_path)
        