import random
from collections import defaultdict
import Id3_dubbed
import copy

def tree_size(root):
    if root is None:
        return 0
    return 1+tree_size(root.left)+tree_size(root.right)

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

def main(test_files):
    examples = defaultdict(list)
    examples1 = defaultdict(list)
    examples2 = defaultdict(list)
    examples3 = defaultdict(list)
    examples4 = defaultdict(list)
    loop = 0
    lst = []
    with open("../Top5000Words/selected-features-indices.txt", 'r') as file:
        for line in file:
            lst.append([int(x) for x in line.split()])
        # rows = [[int(x) for x in line] for line in file]
        # cols = [list(col) for col in zip(*rows)]
        attributes = [x[0] for x in lst]

    with open("../Top5000Words/training-set.feat", 'r') as file:
        for line in file:
            # print(line)
            loop = loop + 1
            words = line.split(' ')
            # print(words[0:1])
            comb = words[1:]
            comb = [int(i.split(':', 1)[0]) for i in comb]
            # print(comb)
            # attributes.sort()
            # print(attributes)
            subt = [x for x in comb if x in attributes]
            # print(subt)
            attr = words[0:1] + subt
            # print(words[0:1][0])
            # print(attr)
            for i in range(len(attr)):
                examples[loop].append(attr[i])
            if int(words[0:1][0]) >= 7:
                examples[loop].append('y')
            else:
                examples[loop].append('n')
    for k, v in examples.items():
        examples[k] = examples[k][1:]
    # print(examples)

    #5 noises
    loop_point = 0
    random_keys = []
    while loop_point < 5:
        key = random.choice(list(examples))
        # print(key)
        random_keys.append(key)
        v = examples[key]
        # print(v)
        if v[len(v)-1] == 'y':
            v[len(v)-1] = 'n'
            examples1[k] = v
        else:
            v[len(v)-1] = 'y'
            examples1[k] = v
        # print(examples1[k])
        loop_point = loop_point+1

    for k, v in examples.items():
        if k not in random_keys:
            examples1[k] = v

    # 10 noises
    loop_point = 0
    random_keys = []
    while loop_point < 10:
        key = random.choice(list(examples))
        # print(key)
        random_keys.append(key)
        v = examples[key]
        # print(v)
        if v[len(v) - 1] == 'y':
            v[len(v) - 1] = 'n'
            examples2[k] = v
        else:
            v[len(v) - 1] = 'y'
            examples2[k] = v
        # print(examples1[k])
        loop_point = loop_point + 1

    for k, v in examples.items():
        if k not in random_keys:
            examples2[k] = v
    # 50 noises
    loop_point = 0
    random_keys = []
    while loop_point < 50:
        key = random.choice(list(examples))
        # print(key)
        random_keys.append(key)
        v = examples[key]
        # print(v)
        if v[len(v) - 1] == 'y':
            v[len(v) - 1] = 'n'
            examples3[k] = v
        else:
            v[len(v) - 1] = 'y'
            examples3[k] = v
        # print(examples1[k])
        loop_point = loop_point + 1

    for k, v in examples.items():
        if k not in random_keys:
            examples3[k] = v
    # 100 noises
    loop_point = 0
    random_keys = []
    while loop_point < 100:
        key = random.choice(list(examples))
        # print(key)
        random_keys.append(key)
        v = examples[key]
        # print(v)
        if v[len(v) - 1] == 'y':
            v[len(v) - 1] = 'n'
            examples4[k] = v
        else:
            v[len(v) - 1] = 'y'
            examples4[k] = v
        # print(examples1[k])
        loop_point = loop_point + 1

    for k, v in examples.items():
        if k not in random_keys:
            examples4[k] = v

    testExamples = defaultdict(list)
    loop = 0
    with open(test_files, 'r') as file:
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
    # print(testExamples)


    # Run ID3
    print("decision tree for 0.5% noise")
    node = Id3_dubbed.decisionTree(examples1, attributes, 0)
    temp = copy.copy(node)
    print("generated decision tree for 0.5% noise")
    print("No. of nodes ",tree_size(temp))
    print("Accuracy on test set")
    print(accuracy(testExamples, node)*100)
    print("decision tree for 1% noise")
    node = Id3_dubbed.decisionTree(examples2, attributes, 0)
    temp = copy.copy(node)
    print("generated decision tree for 1% noise")
    print("No. of nodes ", tree_size(temp))
    print("Accuracy on test set")
    print(accuracy(testExamples, node)*100)
    print("decision tree for 5% noise")
    node = Id3_dubbed.decisionTree(examples3, attributes, 0)
    temp = copy.copy(node)
    print("generated decision tree for 5% noise")
    print("No. of nodes ", tree_size(temp))
    print("Accuracy on test set")
    print(accuracy(testExamples, node)*100)
    print("decision tree for 10% noise")
    node = Id3_dubbed.decisionTree(examples4, attributes, 0)
    temp = copy.copy(node)
    print("generated decision tree for 10% noise")
    print("No. of nodes ", tree_size(temp))
    print("Accuracy on test set")
    print(accuracy(testExamples, node)*100)

if __name__ == '__main__':
    import sys
    testing_data = sys.argv[1]
    print("Adding 0.5, 1, 5, 10% noise in training set and calculating accuracy on test data")
    main(testing_data)

