from collections import defaultdict
import Id3_dubbed
import copy

global total_nodes
total_nodes = 0

def tree_size(root):
    if root is None:
        return 0
    return 1+tree_size(root.left)+tree_size(root.right)

def accuracy(test,node):
    global total_nodes
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
    total_nodes = tree_size(node)
    return accurate/sizes


def prune_tree(root, node, dataset, best_score):
    # if node is a leaf
    if (node.feature == -1):
        # get its classification
        classification = node.sample
        # run validate_tree on a tree with the nodes parent as a leaf with its classification
        ft = node.parent.feature
        lefty = node.parent.left
        righty = node.parent.right
        node.parent.feature = -1
        node.parent.left = None
        node.parent.right = None
        node.parent.sample = node.sample
        new_score = accuracy(dataset, root)
        # if its better, change it
        if (new_score >= best_score):
            return new_score
        else:
            node.parent.feature = ft
            node.parent.sample = -1
            node.parent.left = lefty
            node.parent.right = righty
            return best_score
    # if its not a leaf
    else:
        # prune tree(node.upper_child)
        new_score = prune_tree(root, node.left, dataset, best_score)
        # if its now a leaf, return
        if (node.feature == -1):
            return new_score
        # prune tree(node.lower_child)
        new_score = prune_tree(root, node.right, dataset, new_score)
        # if its now a leaf, return
        if (node.feature == -1):
            return new_score

        return new_score


def main(test_file):
    global total_nodes
    examples = defaultdict(list)
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
            subt = [x for x in comb if x in attributes]
            # print(subt)
            attr = words[0:1] + subt
            for i in range(len(attr)):
                examples[loop].append(attr[i])
            if int(words[0:1][0]) >= 7:
                examples[loop].append('y')
            else:
                examples[loop].append('n')
    for k, v in examples.items():
        examples[k] = examples[k][1:]
    # print(examples)

    testExamples = defaultdict(list)
    loop = 0
    with open(test_file, 'r') as file:
        for line in file:
            # print(line)
            loop = loop + 1
            words = line.split(' ')
            # print(words[0:1])
            comb = words[1:]
            comb = [int(i.split(':', 1)[0]) for i in comb]
            subt = [x for x in comb if x in attributes]
            # print(subt)
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
    print("decision tree for pruning")
    node = Id3_dubbed.decisionTree(examples, attributes, 0)
    print("generated decision tree for pruning")
    temp = copy.copy(node)
    temp1 = copy.copy(node)
    print("No. of nodes ",tree_size(temp))
    best = accuracy(testExamples, node)*100
    print("Best accuracy before pruning on test set ", best)
    print("Pruning on the tree starts")
    new_best = prune_tree(temp1, temp1, testExamples, best)
    print("No. of nodes after pruning on the tree ", total_nodes)
    print("Best accuracy after pruning on test set ", new_best)


if __name__ == '__main__':
    import sys
    testing_data = sys.argv[1]
    print("Pruning decision tree and calculating accuracy on test data")
    main(testing_data)

