import random
import sys
import math

data_file = sys.argv[1]
labels_file = sys.argv[2]

data = []
with open(data_file, "r") as file:
    line = file.readline().strip()
    while line:
        temp = []
        for i in line.split(' '):
            temp.append(float(i))
        temp.append(1)
        data.append(temp)
        line = file.readline().strip()

labels = {}
with open(labels_file, "r") as file:
    line = file.readline().strip()
    while line:
        label = line.split(' ')
        labels[int(label[1])] = int(label[0])
        if (labels.get(int(label[1])) == 0):
            labels[int(label[1])] = -1
        line = file.readline().strip()

w = []
for i in range(0, len(data[0])):
    w.append(0.002 * random.random() - 0.001)

eta = 0.001
stop = 0.001
error = 0
previous_error = 0
iter = 2

def dot_product(x, y):
    product = 0
    for i in range(0, len(x)):
        product += x[i] * y[i]
    return product


while (math.fabs(error - previous_error) > stop or iter > 0):
    iter -= 1
    delf = []
    for i in w:
        delf.append(0)
    for i in range(0, len(data)):
        if(labels.get(i) != None):
            product = dot_product(w, data[i])
            for j in range(0, len(data[0])):
                delf[j] += (labels[i] - product) * data[i][j]

    for i in range(0, len(w)):
        w[i] += eta * delf[i]

    previous_error = error
    error = 0
    
    for i in range(0, len(data)):
        if labels.get(i) != None:
            error += (labels[i] - dot_product(w, data[i])) ** 2
    
# print("w = ", w[:len(w) - 1])

wMod = 0
for i in range(0, len(w)-1):
    wMod += w[i]**2

wMod = math.sqrt(wMod)
dist_origin = math.fabs(w[len(w) - 1] / wMod)
# print("w0/||w||=",dist_origin)

for i in range(0, len(data)):
    if(labels.get(i) == None):
        product = dot_product(w, data[i])
        if(product > 0):
            print(1, i)
        else:
            print(0, i)
