import math, sys

data = []
labels = {}

file_data = sys.argv[1]
file_labels = sys.argv[2]

with open(file_data, "r") as file:
    line = file.readline().strip()
    while line:
        vars = line.split(" ")
        l = []
        for i in vars:
            l.append(float(i))
        data.append(l)
        line = file.readline().strip()

with open(file_labels, "r") as file:
    line = file.readline().strip()
    while line:
        label = line.split(" ")
        labels[int(label[1])] = int(label[0])
        line = file.readline().strip()

m0 = []
n0 = 0
m1 = []
n1 = 0
for i in range(0,len(data[0])):
    m0.append(1)
    m1.append(1)
test_features = []
line_number = []

for i in range(0, len(data)):
    if(labels.get(i) != None and labels.get(i) == 0):
        for j in range(0, len(data[0])):
            m0[j] += data[i][j]
        n0 += 1
    elif(labels.get(i) != None and labels.get(i) == 1):
        for j in range(0, len(data[0])):
            m1[j] += data[i][j]
        n1 += 1
    else:
        test_features.append(data[i])
        line_number.append(i)

for i in range(0, len(m0)):
    m0[i] /= n0
    m1[i] /= n1

std0 = []
std1 = []

for i in range(0, len(data[0])):
    std0.append(0)
    std1.append(0)

for i in range(0, len(data)):
    if(labels.get(i) != None and labels.get(i) == 0):
        for j in range(0, len(data[0])):
            std0[j] += (data[i][j] - m0[j]) ** 2

    elif(labels.get(i) != None and labels.get(i) == 1):
        for j in range(0, len(data[0])):
            std1[j] += (data[i][j] - m1[j]) ** 2

for i in range(0, len(m0)):
    std0[i] /= math.sqrt(std0[i])
    std1[i] /= math.sqrt(std1[i])

for i in range(0, len(test_features)):
    d0 = 0
    d1 = 0
    for j in range(0, len(test_features[0])):
        d0 = d0 + ((test_features[i][j] - m0[j]) / (std0[j])) ** 2
        d1 = d1 + ((test_features[i][j] - m1[j]) / (std1[j])) ** 2

    if (d0 > d1):
        print('1',line_number[i])
    else:
        print('0',line_number[i])
