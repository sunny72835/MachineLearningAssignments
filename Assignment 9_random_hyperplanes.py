import random
import sys
from sklearn import svm

data_file = sys.argv[1]
labels_file = sys.argv[2]

data = []
test_data = []
line_num = 0
labels_list = []

labels = {}
with open(labels_file, "r") as file:
    line = file.readline()
    while line:
        label = line.split()
        l = 1
        if int(label[0]) == 0:
            l = -1
        labels[int(label[1])] = l
        line = file.readline()

with open(data_file, "r") as file:
    line = file.readline()
    while line:
        temp = []
        for i in line.split():
            temp.append(float(i))
        if labels.get(line_num) != None:
            data.append(temp)
        else:
            test_data.append(temp)
        line_num += 1
        line = file.readline()

line_numbers = []
for j in range(0, len(data) + len(test_data)):
    if labels.get(j) != None:
        labels_list.append(labels.get(j))
    else:
        line_numbers.append(j)

k = int(sys.argv[3])

def dot_product(x, y):
    product = 0
    for i in range(0, len(x)):
        product += x[i] * y[i]
    return product

Z = [[0 for i in range(0, k)] for j in range(0, len(data))]
Z_test = [[0 for i in range(0, k)] for j in range(0, len(test_data))]

# Calculation of Z
for iter in range(0, k):
    w = []
    for i in range(0, len(data[0])):
        w.append(random.uniform(-1, 1))

    wx = []
    for j in range(0, len(data)):
        wx.append(dot_product(w, data[j]))
    min = wx[0]
    max = wx[0]
    for i in range(0, len(wx)):
        if(wx[i] < min):
            min = wx[i]
        if(wx[i] > max):
            max = wx[i]
    w0 = random.uniform(min, max)

    zi = []
    for j in range(0, len(data)):
        zi.append(dot_product(data[j], w) + w0)

    for i in range(0, len(data)):
        if zi[i] > 0:
            Z[i][iter] = 1
        else:
            Z[i][iter] = 0

    #Calculation of Z'
    zi_test = []
    for j in range(0, len(test_data)):
        zi_test.append(dot_product(test_data[j], w))
    for i in range(0, len(test_data)):
        Z_test[i][iter] = zi_test[i]

#Classification
clf = svm.LinearSVC(C = 0.001, max_iter=10000)
clf.fit(Z, labels_list)
predict = clf.predict(Z_test)
for i in range(0, len(predict)):
    if predict[i] == -1:
        predict[i] = 0
    print(predict[i], line_numbers[i])