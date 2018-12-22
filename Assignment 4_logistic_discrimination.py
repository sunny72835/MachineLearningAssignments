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
        for i in line.split():
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
        line = file.readline().strip()

w = []
for i in range(0, len(data[0])):
    w.append(0.002 * random.random() - 0.001)

eta = 0.01
stop = 0.0000001
error = 0
previous_error = 0
iter = 2

def dot_product(x, y):
    product = 0
    for i in range(0, len(x)):
        product += x[i] * y[i]
    return product

temp = 0
while (math.fabs(error - previous_error) > stop or iter > 0):
    iter -= 1
    delf = []
    for i in w:
        delf.append(0)
    for i in range(0, len(data)):
        if(labels.get(i) != None):
            temp = (1 / (1 + math.exp(-1 * dot_product(w, data[i]))))
            for j in range(0, len(data[0])):
                delf[j] += (labels[i] - temp) * (data[i][j])

    for i in range(0, len(delf)):
        w[i] += eta * delf[i]

    previous_error = error
    error = 0
    for i in range(0, len(data)):
        if labels.get(i) != None:
            error += labels.get(i)*(math.log(1/(1 + math.exp(-1 * dot_product(w,data[i]))))) +\
                     (1 - labels.get(i)) * math.log(math.exp(-1 * dot_product(w,data[i])) / (1 + math.exp(-1 * dot_product(w,data[i]))))

wMod = 0
for i in range(0, len(w)-1):
    wMod += w[i]**2

# print("w= ", w[0], w[1])

wMod = math.sqrt(wMod)
# print("wMod= ", wMod)
w0 = w[len(w) - 1]
dist_origin = math.fabs(w0 / wMod)
# print("dist_origin= ", dist_origin)

for i in range(0, len(data)):
    if(labels.get(i) == None):
        product = dot_product(w, data[i])
        if(product > 0):
            print(1, i)
        else:
            print(0, i)
