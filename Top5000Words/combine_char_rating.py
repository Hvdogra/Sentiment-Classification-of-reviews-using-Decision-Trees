from random import randint

with open('imdb.txt', 'w') as file3:
    with open('../aclImdb/imdb.vocab', 'r', encoding='utf-8') as file1:
        for line in file1:
            print(line.encode('utf-8'), file=file3)
            # file3.write(line.decode('utf-8'))


infile = open('imdb.txt')
outfile = open("a.txt", "w")
for line in infile:
    outfile.write(line[2:])
    # print(line)
infile.close()
outfile.close()

infile = open('a.txt')
outfile = open("b.txt", "w")
for line in infile:
    outfile.write(line[:-4]+"\n")
infile.close()
outfile.close()

# import re
# string = open('imdb.txt').read()
# new_str = re.sub('[^a-zA-Z0-9\n\.]', ' ', string)
# open('b.txt', 'w').write(new_str)
index = 0
with open('combined_text_rating.txt', 'w') as file3:
    with open('b.txt', 'r') as file1:
        with open('../aclImdb/imdbEr.txt', 'r', encoding="utf8") as file2:
            for line1, line2 in zip(file1, file2):
                print(str(index), line1.strip(), line2.strip(), file=file3)
                index=index+1

with open('combined_text_rating.txt') as f:
    lines = [line.split(' ') for line in f]
output = open("sorted_data.txt", 'w')

for line in sorted(lines, key=lambda d: float(d[2])):
    output.write(' '.join(line))

output.close()

val=0
f = open('selected-features-indices.txt','w')
ff = open('sorted_data.txt','r')
lines=ff.readlines()
indexDict = {}
repeated = {}
loop_variable=0
for x in lines:
    indexDict[loop_variable] = x.split(' ')[0]
    loop_variable = loop_variable+1

iterations = 5000
while iterations > 0:
    value = randint(0, 89258)
    if value not in repeated:
        f.write(indexDict[value]+'\n')
        iterations = iterations-1
    repeated[value] = 1
f.close()
# fff = open('selected-features-indices.txt','r')
# lines=fff.readlines()
# for x in lines:
#     print(x)
from itertools import islice

infile = open('../aclImdb/train/labeledBow.feat','r')
outfile = open('training-set.feat','w')
with open('../aclImdb/train/labeledBow.feat','r') as myfile:
    for line in islice(myfile, 500):
        # print(line)
        outfile.write(line)

# import sys
# import os
# bufsize = 8192
# fsize = os.stat('../aclImdb/train/labeledBow.feat').st_size
# iter = 0
# with open('../aclImdb/train/labeledBow.feat') as f:
#     if bufsize > fsize:
#         bufsize = fsize-1
#         data = []
#         while True:
#             iter +=1
#             f.seek(fsize-bufsize*iter)
#             data.extend(f.readlines())
#             if len(data) >= 500 or f.tell() == 0:
#                 outfile.write(''.join(data[-500:]))
#                 break

with open('../aclImdb/train/labeledBow.feat','r') as f:
    cc=f.readlines()[-500:]
    for line in cc:
        outfile.write(line)

infile = open('../aclImdb/train/labeledBow.feat','r')
outfile = open('test-set.feat','w')
with open('../aclImdb/test/labeledBow.feat','r') as myfile:
    for line in islice(myfile, 500):
        # print(line)
        outfile.write(line)

with open('../aclImdb/train/labeledBow.feat', 'r') as f:
    cc = f.readlines()[-500:]
    for line in cc:
        outfile.write(line)
