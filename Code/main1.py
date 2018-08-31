import os
from collections import defaultdict
import Id3_dubbed
import copy

def accuracy(test,node):
    accurate = 0
    sizes = len(test)
    for k,v in test.items():
        temp = copy.copy(node)
        while temp.feature != -1:
            if temp.feature in v:
                temp = temp.right
            else:
                temp = temp.left
        if v[len(v)-1] == 'y':
            if temp.sample == 1:
                accurate = accurate+1
        else:
            if temp.sample == 0:
                accurate = accurate+1
    # print(accurate)
    return accurate/sizes

def main(test_set):
    examples = defaultdict(list)
    loop = 0
    lst = []
    with open("../Top5000Words/selected-features-indices.txt", 'r') as file:
        for line in file:
            lst.append([int(x) for x in line.split()])
        attributes = [x[0] for x in lst]

    with open("../Top5000Words/training-set.feat", 'r') as file:
        for line in file:
            # print(line)
            loop = loop + 1
            words = line.split(' ')
            comb = words[1:]
            comb = [int(i.split(':', 1)[0]) for i in comb]
            subt = [x for x in comb if x in attributes]
            attr = words[0:1] + subt
            for i in range(len(attr)):
                examples[loop].append(attr[i])
            if int(words[0:1][0]) >= 7:
                examples[loop].append('y')
            else:
                examples[loop].append('n')
    for k, v in examples.items():
        examples[k] = examples[k][1:]

    testExamples = defaultdict(list)
    loop = 0
    with open(test_set, 'r') as file:
        for line in file:
            loop = loop + 1
            words = line.split(' ')
            comb = words[1:]
            comb = [int(i.split(':', 1)[0]) for i in comb]
            subt = [x for x in comb if x in attributes]
            attr = words[0:1] + subt
            for i in range(len(attr)):
                testExamples[loop].append(attr[i])
            if int(words[0:1][0]) >= 7:
                testExamples[loop].append('y')
            else:
                testExamples[loop].append('n')
    for k, v in testExamples.items():
        testExamples[k] = testExamples[k][1:]


    # Run ID3
    node = Id3_dubbed.decisionTree(examples, attributes, 0)
    print("generated decision tree")
    print("Accuracy in test set ")
    print(accuracy(testExamples, node)*100)

if __name__ == '__main__':
    import sys
    if sys.argv[2] == "2":
        print("Using training data to learn decision tree and calculating accuracy on training data")
        main(sys.argv[1])
        os.system('python id3_2.py '+sys.argv[1])
    elif sys.argv[2] == "3":
        os.system('python id3_3.py ' + sys.argv[1])
    elif sys.argv[2] == "4":
        os.system('python id3_4.py ' + sys.argv[1])
    elif sys.argv[2] == "5":
        os.system('python id3_5.py ' + sys.argv[1])