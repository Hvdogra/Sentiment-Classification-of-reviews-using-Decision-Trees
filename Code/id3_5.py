from collections import defaultdict
import Id3_dubbed
import copy

def get_valid_examples(attributes):
    examples = defaultdict(list)
    loop = 0
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
    return examples


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

def accuracy2(test,node, node1, node2):
    accurate = 0
    sizes = len(test)
    for k,v in test.items():
        temp = copy.copy(node)
        temp1 = copy.copy(node1)
        temp2 = copy.copy(node2)
        while temp.feature != -1:
            if temp.feature in v:
                temp = temp.right
            else:
                temp = temp.left
        while temp1.feature != -1:
            if temp1.feature in v:
                temp1 = temp1.right
            else:
                temp1 = temp1.left
        while temp2.feature != -1:
            if temp2.feature in v:
                temp2 = temp2.right
            else:
                temp2 = temp2.left
        count1 = 0
        count2 = 0
        if temp.sample == 1:
            count1 = count1+1
        else:
            count2 = count2+1
        if temp1.sample == 1:
            count1 = count1 + 1
        else:
            count2 = count2 + 1
        if temp2.sample == 1:
            count1 = count1 + 1
        else:
            count2 = count2 + 1

        if count1 >= count2:
            temp.sample = 1
        else:
            temp.sample = 0
        if v[len(v)-1] == 'y':
            if temp.sample == 1:
                accurate = accurate+1
        else:
            if temp.sample == 0:
                accurate = accurate+1
    # print(accurate)
    return accurate/sizes

def accuracy3(test,node, node1, node2, node3, node4):
    accurate = 0
    sizes = len(test)
    for k,v in test.items():
        temp = copy.copy(node)
        temp1 = copy.copy(node1)
        temp2 = copy.copy(node2)
        temp3 = copy.copy(node3)
        temp4 = copy.copy(node4)
        while temp.feature != -1:
            if temp.feature in v:
                temp = temp.right
            else:
                temp = temp.left
        while temp1.feature != -1:
            if temp1.feature in v:
                temp1 = temp1.right
            else:
                temp1 = temp1.left
        while temp2.feature != -1:
            if temp2.feature in v:
                temp2 = temp2.right
            else:
                temp2 = temp2.left
        while temp3.feature != -1:
            if temp3.feature in v:
                temp3 = temp3.right
            else:
                temp3 = temp3.left

        while temp4.feature != -1:
            if temp4.feature in v:
                temp4 = temp4.right
            else:
                temp4 = temp4.left
        count1 = 0
        count2 = 0
        if temp.sample == 1:
            count1 = count1+1
        else:
            count2 = count2+1
        if temp1.sample == 1:
            count1 = count1 + 1
        else:
            count2 = count2 + 1
        if temp2.sample == 1:
            count1 = count1 + 1
        else:
            count2 = count2 + 1
        if temp3.sample == 1:
            count1 = count1 + 1
        else:
            count2 = count2 + 1
        if temp4.sample == 1:
            count1 = count1 + 1
        else:
            count2 = count2 + 1

        if count1 >= count2:
            temp.sample = 1
        else:
            temp.sample = 0
        if v[len(v)-1] == 'y':
            if temp.sample == 1:
                accurate = accurate+1
        else:
            if temp.sample == 0:
                accurate = accurate+1
    # print(accurate)
    return accurate/sizes

def main(test_file):
    loop = 0
    lst = []
    with open("../Top5000Words/selected-features-indices.txt", 'r') as file:
        for line in file:
            lst.append([int(x) for x in line.split()])
        attributes = [x[0] for x in lst]
    attributes2_1 = []
    attributes2_1[0:1250] = attributes[0:1250]
    attributes2_1[1250:2500] = attributes[2500:3750]
    attributes2_2 = []
    attributes2_2[0:1250] = attributes[1250:2500]
    attributes2_2[1250:2500] = attributes[3750:5000]
    attributes2_3 = []
    attributes2_3[0:1250] = attributes[0:1250]
    attributes2_3[1250:2500] = attributes[3750:5000]

    attributes3_1 = []
    attributes3_1[0:500] = attributes[0:500]
    attributes3_1[500:1000] = attributes[2500:3000]
    attributes3_2 = []
    attributes3_2[0:500] = attributes[500:1000]
    attributes3_2[500:1000] = attributes[3000:3500]
    attributes3_3 = []
    attributes3_3[0:500] = attributes[1000:1500]
    attributes2_1[500:1000] = attributes[3500:4000]
    attributes3_4 = []
    attributes3_4[0:500] = attributes[1500:2000]
    attributes3_4[500:1000] = attributes[4000:4500]
    attributes3_5 = []
    attributes3_5[0:500] = attributes[2000:2500]
    attributes3_5[500:1000] = attributes[4500:5000]
    # print(attributes2_1)

    examples = get_valid_examples(attributes)
    examples2_1 = get_valid_examples(attributes2_1)
    examples2_2 = get_valid_examples(attributes2_2)
    examples2_3 = get_valid_examples(attributes2_3)
    examples3_1 = get_valid_examples(attributes3_1)
    examples3_2 = get_valid_examples(attributes3_2)
    examples3_3 = get_valid_examples(attributes3_3)
    examples3_4 = get_valid_examples(attributes3_4)
    examples3_5 = get_valid_examples(attributes3_5)
    testExamples = defaultdict(list)
    loop = 0
    with open(test_file, 'r') as file:
        for line in file:
            loop = loop + 1
            words = line.split(' ')
            # print(words[0:1])
            comb = words[1:]
            comb = [int(i.split(':', 1)[0]) for i in comb]
            subt = [x for x in comb if x in attributes]
            # print(subt)
            attr = words[0:1] + subt
            # print(words[0:1][0])
            # print(attr)
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
    print("1 decision tree of 5k attributes")
    node = Id3_dubbed.decisionTree(examples, attributes, 0)
    # temp = copy.copy(node)
    # print("No. of nodes",tree_size(temp))
    print("generated decision tree")
    # print("Accuracy on test set is ", accuracy(testExamples, node)*100)
    # print("Accuracy on training set is ", accuracy(examples, node)*100)
    print("1    ",accuracy(examples, node)*100,"    ", accuracy(testExamples, node)*100)
    print("3 decision trees of 2.5k attributes each")
    node = Id3_dubbed.decisionTree(examples2_1, attributes2_1, 0)
    node1 = Id3_dubbed.decisionTree(examples2_2, attributes2_2, 0)
    node2 = Id3_dubbed.decisionTree(examples2_3, attributes2_3, 0)
    # temp = copy.copy(node)
    # print("No. of nodes", tree_size(temp))
    print("generated decision tree")
    # print("Accuracy on test set is ", accuracy2(testExamples, node, node1, node2)*100)
    # print("Accuracy on training set is ", accuracy2(examples, node, node1, node2)*100)
    print("3    ", accuracy2(examples, node, node1, node2)*100, "    ", accuracy2(testExamples, node, node1, node2)*100)
    print("5 decision trees of 1k attributes each")
    node = Id3_dubbed.decisionTree(examples3_1, attributes3_1, 0)
    node1 = Id3_dubbed.decisionTree(examples3_2, attributes3_2, 0)
    node2 = Id3_dubbed.decisionTree(examples3_3, attributes3_3, 0)
    node3 = Id3_dubbed.decisionTree(examples3_4, attributes3_4, 0)
    node4 = Id3_dubbed.decisionTree(examples3_5, attributes3_5, 0)
    # temp = copy.copy(node)
    # print("No. of nodes", tree_size(temp))
    print("generated decision tree")
    # print("Accuracy on test set is ", accuracy3(testExamples, node, node1, node2, node3, node4)*100)
    # print("Accuracy on training set is ", accuracy3(examples, node, node1, node2, node3, node4)*100)
    print("5    ", accuracy3(examples, node, node1, node2, node3, node4)*100,"  ",accuracy3(testExamples, node, node1, node2, node3, node4)*100)
if __name__ == '__main__':
    import sys
    testing_data = sys.argv[1]
    print("Learning Random Forest using Feature Bagging and calculating accuracy on training and test data")
    print("result will be displayed as")
    print("No. of Trees     Training Accuracy      Testing Accuracy")
    main(testing_data)

