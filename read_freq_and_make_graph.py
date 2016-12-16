import os
import sys
import string
import json
import operator
import numpy as np
import pickle as pk
from pprint import pprint
import threading

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

def worker(num):
    """thread worker function"""
    global data
    global arr
    print 'Worker: %s' % num

    # count = 0
    for i in range(len(data)):
        if i%4 == num:
            print("%d th element" %i)
            for j in range(len(data)):
                for k in data[i]:
                    for l in data[j]:
                        # for m in data[i][k]['did']:
                        #     if m in data[j][l]['did']:
                        #         count+=1
                        if i == j :
                            arr[i][j] = len(set(data[i][k]['did'].keys()))
                        else:
                            arr[i][j] = arr[j][i] = len(set(data[i][k]['did'].keys()).intersection(set(data[j][l]['did'].keys())))
                        # arr[i][j] = arr[j][i] = count
                        # count = 0

threads = []


subdirs = get_immediate_subdirectories(walk_dir)
total_number_of_files = 517401

for walk_subdir in subdirs:
    absolute_path = os.path.join(walk_dir, walk_subdir)
    print(absolute_path)
    count = 0

    for root, subdirs, files in os.walk(absolute_path):
        # print("changing folder"+root)
        new_files = []
        for filename in files:
            if filename == 'freq_dict-1.json' :
                file_path = os.path.join(root, filename)

                with open(file_path, 'rb') as data_file:    
                    data = json.load(data_file)
                
                total_number_of_files = data[0]['total_number_of_files']
            
            else:
                new_files.append(filename)
                continue
        
        files = new_files
        print total_number_of_files
        for filename in files:
            file_path = os.path.join(root, filename)

            with open(file_path, 'rb') as data_file:    
                data = json.load(data_file)

            arr = np.zeros((len(data), len(data)))

            # for i in range(4):
            #     t = threading.Thread(target=worker, args=(i,))
            #     threads.append(t)
            #     t.start()

            # for thread in threads:
            #     thread.join()

            for i in range(len(data)):
                # print("%d th element" %i)
                for j in range(len(data)):
                    for k in data[i]:
                        for l in data[j]:
                            if i == j :
                                arr[i][j] = len(set(data[i][k]['did'].keys()))
                            else:
                                arr[i][j] = arr[j][i] = len(set(data[i][k]['did'].keys()).intersection(set(data[j][l]['did'].keys())))
                            arr[i][j] /= total_number_of_files
                            arr[j][i] /= total_number_of_files


            print("dumping....")
            output_usr_dir = os.path.join(output_dir, walk_subdir)
            output_file_path = output_usr_dir+'/g'
            if not os.path.exists(os.path.dirname(output_file_path)):
                os.makedirs(os.path.dirname(output_file_path))
            op = open(output_file_path, 'w')
            np.save(op, arr)