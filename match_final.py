import os
import sys
import string

file_k = sys.argv[1]
file_t = sys.argv[2]
output_file_path = sys.argv[3]

# file_p = os.path.join(root, filename)
with open(file_p, 'rb') as f:
    f_p = f.readlines()

# file_t = os.path.join(root, filename)
with open(file_t, 'rb') as f:
    f_t = f.readlines()

f_t1 = range(len(f_t))

print(f_t1)

count=0
for idx in file_k:
    idx=idx.strip()

    f_t1[int(idx)-1] = f_t[count].strip()
    count+=1

if not os.path.exists(os.path.dirname(output_file_path)):
    os.makedirs(os.path.dirname(output_file_path))
op = open(output_file_path, 'w')
write_Content = '\n'.join(f_t1)
op.write(write_Content)
