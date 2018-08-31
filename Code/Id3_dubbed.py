import math
from collections import defaultdict
from Node import Node

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

    # print(dataEntropy)
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
    # print("i is ",i)
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
                    # if v[len(v) - 1] == val:
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
    # print(best)
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
    node = Node()
    recursion += 1
    # print(data)
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
        if default == 'y':
            node.sample = 1
            return node
        else:
            node.sample = 0
            return node
    # If all the records in the dataset have the same classification,
    # return that classification.
    elif allYes == 1:
        node.sample = 1
        return node
    elif allNo == 1:
        node.sample = 0
        return node
    else:
        # Choose the next best attribute to best classify our data
        best = chooseAttr(data, attributesGiven)
        print("Attribute for splitting ",best)
        if best == -1:
            if default == 'y':
                node.sample = 1
                return node
            else:
                node.sample = 0
                return node

        for val in getValues(data, attributesGiven, best):
            # Create a subtree for the current value under the "best" field
            exampleSubset = getExamples(data, attributesGiven, best, val)
            newAttr = attributesGiven[:]
            newAttr.remove(best)
            if val == 'y':
                node.right = decisionTree(exampleSubset, newAttr, recursion)
                if node.right is not None:
                    node.right.parent = node
            else:
                node.left = decisionTree(exampleSubset, newAttr, recursion)
                if node.left is not None:
                    node.left.parent = node

    node.feature = best
    return node


