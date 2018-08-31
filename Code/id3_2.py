import math
from collections import defaultdict
from Node import Node
import copy

global terminal_nodes
terminal_nodes = 0
global char_map
char_map = {}
global attr_count
attr_count = {}
def majority(data):
    valFreq = {}
    for k, v in data.items():
        if v[len(v) - 1] in valFreq:
            valFreq[v[len(v) - 1]] += 1.0
        else:
            valFreq[v[len(v) - 1]] = 1.0
    max = 0
    major = ""
    for key in valFreq.keys():
        if valFreq[key] > max:
            max = valFreq[key]
            major = key
    return major


# Calculates the entropy of the given data set for the target attr
def entropy(data):
    valFreq = {}
    dataEntropy = 0.0

    # Calculate the frequency of each of the values in the target attr
    for k, v in data.items():
        if v[len(v) - 1] in valFreq:
            valFreq[v[len(v) - 1]] += 1.0
        else:
            valFreq[v[len(v) - 1]] = 1.0

    # Calculate the entropy of the data for the target attr
    for freq in valFreq.values():
        dataEntropy += (-freq / len(data)) * math.log(freq / len(data), 2)

    return dataEntropy


def gain(attributes, data, attr):
    """
    Calculates the information gain (reduction in entropy) that would
    result by splitting the data on the chosen attribute (attr).
    """
    valFreq = {}
    subsetEntropy = 0.0

    # find index of the attribute
    i = attributes.index(attr)
    # Calculate the frequency of each of the values in the target attribute
    for k, v in data.items():
        if attr in v:
            if 'y' in valFreq:
                valFreq['y'] += 1.0
            else:
                valFreq['y'] = 1.0
        else:
            if 'n' in valFreq:
                valFreq['n'] += 1.0
            else:
                valFreq['n'] = 1.0
    # Calculate the sum of the entropy for each subset of records weighted
    # by their probability of occuring in the training set.
    for val in valFreq.keys():
        valProb = valFreq[val] / sum(valFreq.values())
        dataSubset = defaultdict(list)
        for k, v in data.items():
            if val == 'y':
                if attr in v:
                    for i in range(len(v)):
                        if v[i] != attr:
                            dataSubset[k].append(v[i])
            else:
                if attr not in v:
                    for i in range(len(v)):
                        dataSubset[k].append(v[i])
        subsetEntropy += valProb * entropy(dataSubset)

    # Subtract the entropy of the chosen attribute from the entropy of the
    # whole data set with respect to the target attribute (and return it)
    # print(entropy(data))
    return entropy(data) - subsetEntropy


# choose best attibute
def chooseAttr(data, attributes):
    best = -1
    maxGain = 0;
    for attr in attributes:
        newGain = gain(attributes, data, attr)
        if newGain > maxGain:
            maxGain = newGain
            best = attr
    return best


def getValues(data, attributes, attr):
    values = []
    for k, v in data.items():
        if attr in v:
            if 'y' not in values:
                values.append('y')
        else:
            if 'n' not in values:
                values.append('n')
    return values


def getExamples(data, attributes, best, val):
    exampled = defaultdict(list)
    for k, v in data.items():
        # find entries with the give value
        if val == 'y':
            if best in v:
                for i in range(len(v)):
                    if v[i] != best:
                        exampled[k].append(v[i])
        else:
            if best not in v:
                for i in range(len(v)):
                    exampled[k].append(v[i])
    return exampled


def decisionTree(data, attributesGiven, recursion):
    global terminal_nodes
    global attr_count
    global char_map
    node = Node()
    recursion += 1
    allYes = 1
    allNo = 1
    for k, v in data.items():
        if v[len(v) - 1] != 'y':
            allYes = 0
    for k, v in data.items():
        if v[len(v) - 1] != 'n':
            allNo = 0
    default = majority(data)

    # If the dataset is empty or the attributes list is empty, return the
    # default value. When checking the attributes list for emptiness, we
    # need to subtract 1 to account for the target attribute.
    if (not data) or (len(attributesGiven) - 1) <= 0:
        # print("variant")
        if default == 'y':
            node.sample = 1
            terminal_nodes = terminal_nodes+1
            return node
        else:
            node.sample = 0
            terminal_nodes = terminal_nodes + 1
            return node
    # If all the records in the dataset have the same classification,
    # return that classification.
    elif allYes == 1:
        node.sample = 1
        terminal_nodes = terminal_nodes + 1
        return node
    elif allNo == 1:
        node.sample = 0
        terminal_nodes = terminal_nodes + 1
        return node
    elif len(data) < 50:
        if default == 'y':
            node.sample = 1
            terminal_nodes = terminal_nodes+1
            return node
        else:
            node.sample = 0
            terminal_nodes = terminal_nodes + 1
            return node
    else:
        # Choose the next best attribute to best classify our data
        best = chooseAttr(data, attributesGiven)
        print("Attribute for splitting ", best)
        if char_map[best] in attr_count:
            attr_count[char_map[best]] = attr_count[char_map[best]]+1
        else:
            attr_count[char_map[best]] = 1
        if best == -1:
            if default == 'y':
                node.sample = 1
                terminal_nodes = terminal_nodes + 1
                return node
            else:
                node.sample = 0
                terminal_nodes = terminal_nodes + 1
                return node

        for val in getValues(data, attributesGiven, best):
            # Create a subtree for the current value under the "best" field
            exampleSubset = getExamples(data, attributesGiven, best, val)
            newAttr = attributesGiven[:]
            newAttr.remove(best)
            if val == 'y':
                node.right = decisionTree(exampleSubset, newAttr, recursion)
            else:
                node.left = decisionTree(exampleSubset, newAttr, recursion)


    node.feature = best
    return node



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
    return accurate/sizes

def main(test_file):
    global terminal_nodes
    global char_map
    global attr_count

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
        outfile.write(line[:-4] + "\n")
    infile.close()
    outfile.close()

    looping = 1
    infile = open('b.txt')
    for line in infile:
        char_map[looping] = line[:-1]
        looping = looping+1

    examples = defaultdict(list)
    loop = 0
    lst = []
    with open("../Top5000Words/selected-features-indices.txt", 'r') as file:
        for line in file:
            lst.append([int(x) for x in line.split()])
        attributes = [x[0] for x in lst]

    with open("../Top5000Words/training-set.feat", 'r') as file:
        for line in file:
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
    with open(test_file, 'r') as file:
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
    node = decisionTree(examples, attributes, 0)
    print("generated decision tree")
    print("Terminal nodes count is ",terminal_nodes)
    print("Accuracy on Test set is")
    print(accuracy(testExamples, node)*100)
    for k, v in attr_count.items():
        print(k,v)

if __name__ == '__main__':
    import sys
    testing_data = sys.argv[1]
    print("Using early stopping of less than 50 examples in a node and calculating accuracy on test data")
    main(testing_data)

