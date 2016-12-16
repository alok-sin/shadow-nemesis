import os
import sys
import string
from nltk.tokenize import TreebankWordTokenizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

stops = set(stopwords.words('english'))
stemmer = SnowballStemmer("english")
tokenizer = TreebankWordTokenizer()
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
            print (file_path)
            f_content = f.readlines()
            a = [i for i, s in enumerate(f_content) if 'X-FileName:' in s]
            if len(a) == 1:
                text_content = '\n'.join(f_content[a[0]+1:])
               	text_content = text_content.translate(None, string.punctuation)
               	words = tokenizer.tokenize(text_content)
               	words = [word.lower() for word in words]
                stemmed = [stemmer.stem(w) for w in words]
               	removedWords = [w for w in stemmed if w not in stops]
            else:
                print (file_path)
                #sys.exit()
            output_file_path = file_path.replace(walk_dir, output_dir)
            if not os.path.exists(os.path.dirname(output_file_path)):
                os.makedirs(os.path.dirname(output_file_path))
            op = open(output_file_path, 'w')
            write_Content = '\n'.join(removedWords)
            op.write(write_Content)