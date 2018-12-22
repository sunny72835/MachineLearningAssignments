import random
import sys
import math

data_file = sys.argv[1]
labels_file = sys.argv[2]

data = []
with open(data_file, "r") as file:
    line = file.readline()
    while line:
        temp = []
        for i in line.split():
            temp.append(float(i))
        temp.append(1)
        data.append(temp)
        line = file.readline()

labels = {}
with open(labels_file, "r") as file:
    line = file.readline()
    while line:
        label = line.split()
        labels[int(label[1])] = int(label[0])
        if (labels.get(int(label[1])) == 0):
            labels[int(label[1])] = -1
        line = file.readline()

w = []
for i in range(0, len(data[0])):
    w.append(0.002 * random.random() - 0.001)

eta_list = [1, .1, .01, .001, .0001, .00001, .000001, .0000001, .00000001, .000000001, .0000000001, .00000000001]
best_eta = 0
prev_obj = 0
bestobj = 1000000000000
stop = 0.001
error = 0
previous_error = 0
iter = 2

def dot_product(x, y):
    product = 0
    for i in range(0, len(x)):
        product += x[i] * y[i]
    return product

temp = 0
while (math.fabs(bestobj - prev_obj) > stop or iter > 0):
    iter -= 1
    prev_obj = bestobj
    delf = []

    for i in w:
        delf.append(0)
    for i in range(0, len(data)):
        if (labels.get(i) != None):
            temp = labels[i] * (dot_product(w, data[i]))
            if temp < 1:
                for j in range(0, len(data[0])):
                    delf[j] += data[i][j] * labels[i]
    for k in range(0, len(eta_list)):
        eta = eta_list[k]
        for i in range(0, len(delf)):
            w[i] += eta * delf[i]

        error = 0
        for i in range(0, len(data)):
            if labels.get(i) != None:
                temp = 1 - (labels[i] * (dot_product(w, data[i])))
                if(temp > 0):
                    error += temp
        for i in range(0, len(delf)):
            w[i] -= eta * delf[i]
        if error <= bestobj:
            bestobj = error
            best_eta = eta
        # print(bestobj)
    for i in range(0, len(w)):
        w[i] += best_eta * delf[i]
    error = 0
    for i in range(0, len(data)):
        if labels.get(i) != None:
            temp = 1 - (labels[i] * (dot_product(w, data[i])))
            if (temp > 0):
                error += temp
    bestobj = error
    # print("Error= ", error)

wMod = 0
for i in range(0, len(w)-1):
    wMod += w[i]**2

wMod = math.sqrt(wMod)
w0 = w[len(w) - 1]
dist_origin = math.fabs(w0 / wMod)

for i in range(0, len(data)):
    if(labels.get(i) == None):
        product = dot_product(w, data[i])
        if(product > 0):
            print(1, i)
        else:
            print(0, i)
