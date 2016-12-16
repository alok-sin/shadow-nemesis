from __future__ import division
import os
import sys
import string
import json
import binascii
from random import shuffle

from Crypto.Hash import HMAC, SHA

key = b'enron_secret_key'

def hmac_sha256(key, msg):
    hash_obj = HMAC.new(key=key, msg=msg, digestmod=SHA)
    return hash_obj.hexdigest()
# file_p = sys.argv[1]
# file_t = sys.argv[2]
# output_file_path = sys.argv[3]
walk_dir = sys.argv[1]
keyword_size = 100
keys_directory = '/home/alok/Projects/security/test/topKeys/'
tags_directory = '/home/alok/Projects/security/test/topTags/'
# file_p = os.path.join(root, filename)
# with open(file_p, 'rb') as f:
#     f_p = f.readlines()


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
        if os.path.isdir(os.path.join(a_dir, name))]

def read_json(file_path):
    with open(file_path, 'rb') as data_file:    
        data = json.load(data_file)
        return data



def write_to_file(output_file_path, list_data):
    if not os.path.exists(os.path.dirname(output_file_path)):
        os.makedirs(os.path.dirname(output_file_path))
    op = open(output_file_path, 'w')
    write_Content = '\n'.join(list_data)
    op.write(write_Content)

subdirs = get_immediate_subdirectories(walk_dir)

matched_records = []
u_match = []
p_match = []
u_records = []
p_records = []

naive_matched_records = []
ume_matched_records = []
path_matched_records = []

for walk_subdir in subdirs:
    json_key_path = os.path.join(keys_directory, walk_subdir)+'/freq_dict-0.json'
    json_tag_path = os.path.join(tags_directory, walk_subdir)+'/freq_dict-0.json'

    keys = read_json(json_key_path)
    keys = keys[0:keyword_size]
    keys = [obj.keys()[0] for obj in keys]

    tags = read_json(json_tag_path)
    tags = tags[0:keyword_size]
    tags = [obj.keys()[0] for obj in tags]


    perm_file_path = os.path.join(walk_dir, walk_subdir)+'/exp_out_file'
    with open(perm_file_path, 'rb') as f:
        f_content = f.readlines()
        a = [i for i, s in enumerate(f_content) if 'Permutations' in s]
        if len(a) == 1:
            f_content = f_content[a[0]+2:]
            f_content = [x.strip() for x in f_content]
            list2 = [x.split(' ') for x in f_content]

            umeyama = [each_list[0] for each_list in list2]
            path = [each_list[1] for each_list in list2]

            f_t1 = range(len(path))
            f_t2 = range(len(path))

            for i in range(len(umeyama)):
                uidx=umeyama[i].strip()
                f_t1[int(uidx)-1] = tags[i].strip()

                pidx=path[i].strip()
                f_t2[int(pidx)-1] = tags[i].strip()

            hashed_keys = [hmac_sha256(key, keyword.strip()) for keyword in keys]

            u_match = []
            p_match = []
            naive_match = []
            for i in range(len(tags)):
                if hashed_keys[i] == f_t1[i]:
                    u_match.append(keys[i])
                if hashed_keys[i] == f_t2[i]:
                    p_match.append(keys[i])
                if hashed_keys[i] == tags[i]:
                    naive_match.append(keys[i])
                

            matches = list(set(tags).intersection(set(hashed_keys)))
            
            matching_keys = []

            for match in matches:
                matching_keys.append(keys[hashed_keys.index(match)])

            # matched_records.append(walk_subdir+" "+str(len(matches)))
            u_records.append(walk_subdir+' '+str(len(u_match)))
            p_records.append(walk_subdir+' '+str(len(p_match)))

            # output_key_path = os.path.join(walk_dir, walk_subdir)+'/keys'
            # output_tag_path = os.path.join(walk_dir, walk_subdir)+'/tags'
            # output_ume_path = os.path.join(walk_dir, walk_subdir)+'/ume'
            # output_path_path = os.path.join(walk_dir, walk_subdir)+'/path'
            # output_mkey_path = os.path.join(walk_dir, walk_subdir)+'/all_matching_keys'
            # output_mkey_path = os.path.join(walk_dir, walk_subdir)+'/hashed_keys'

            # write_to_file(output_key_path, keys)
            # write_to_file(output_mkey_path, matching_keys)
            # write_to_file(output_tag_path, tags)
            # write_to_file(output_ume_path, f_t1)
            # write_to_file(output_path_path, f_t2)
            a = len(naive_match)/len(matches)*100
            naive_matched_records.append(float("{0:.2f}".format(a)))

            a = len(u_match)/len(matches)*100
            ume_matched_records.append(float("{0:.2f}".format(a)))

            a = len(p_match)/len(matches)*100
            path_matched_records.append(float("{0:.2f}".format(a)))

naive_records_fp = os.path.join(walk_dir)+'/naive'
u_records_fp = os.path.join(walk_dir)+'/ume'
p_records_fp = os.path.join(walk_dir)+'/path'

naive_matched_records.sort()
naive_matched_records = [str(x) for x in naive_matched_records]

ume_matched_records.sort()
ume_matched_records = [str(x) for x in ume_matched_records]

path_matched_records.sort()
path_matched_records = [str(x) for x in path_matched_records]

print("Freq. matching")
print('\t'.join(map(str,naive_matched_records)))
# print(naive_matched_records)
print("Umeyama matching")
print('\t'.join(map(str,ume_matched_records)))
print("Path matching")
print('\t'.join(map(str,path_matched_records)))
# write_to_file(naive_records_fp, naive_matched_records)
# write_to_file(u_records_fp, ume_matched_records)
# write_to_file(p_records_fp, path_matched_records)
            
