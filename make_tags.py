import os
import sys
import string
import binascii
from random import shuffle

from Crypto.Hash import HMAC, SHA

key = b'enron_secret_key'

def hmac_sha256(key, msg):
    hash_obj = HMAC.new(key=key, msg=msg, digestmod=SHA)
    return hash_obj.hexdigest()

walk_dir = sys.argv[1]
output_dir = sys.argv[2]

print('walk_dir = ' + walk_dir)

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

for root, subdirs, files in os.walk(walk_dir):

    for filename in files:
        file_path = os.path.join(root, filename)

        with open(file_path, 'rb') as f:
            f_content = f.readlines()
            
            removedWords = [hmac_sha256(key, keyword.strip()) for keyword in f_content]

            # remove count pattern and keyword-occurence pattern. L4->L2
            removedWords = list(set(removedWords))
            shuffle(removedWords)

            output_file_path = file_path.replace(walk_dir, output_dir)
            if not os.path.exists(os.path.dirname(output_file_path)):
                os.makedirs(os.path.dirname(output_file_path))
            op = open(output_file_path, 'w')
            write_Content = '\n'.join(removedWords)
            op.write(write_Content)