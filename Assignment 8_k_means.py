import sys
import random

data_file = sys.argv[1]
K = int(sys.argv[2])
# if len(sys.argv) > 2:
#     labels_file = sys.argv[3]

data = []

with open(data_file, "r") as file:
    line = file.readline()
    while line:
        temp = []
        for i in line.split():
            temp.append(float(i))
        data.append(temp)
        line = file.readline()
# if(labels_file != None):
#     labels = {}
#     with open(labels_file, "r") as file:
#         line = file.readline()
#         while line:
#             label = line.split()
#             labels[int(label[1])] = int(label[0])
#             if (labels.get(int(label[1])) == 0):
#                 labels[int(label[1])] = -1
#             line = file.readline()

# Initialization:
C ={}
count_class = [0 for i in range(0, K)]
for i in range(0, len(data)):
    C[i] = i % K
    count_class[i % K] += 1

mean = []
for i in range(0, K):
    mean.append([0 for j in range(0, len(data[0]))])

for i in range(0, len(data)):
    for j in range(0, len(data[0])):
        mean[C.get(i)][j] += data[i][j]

for i in range(0, len(mean)):
    for j in range(0, len(data[0])):
        mean[i][j] /= count_class[i]

error = 0
previous_error = 0
iter = 1
counter = 0
variance = [0 for i in range(0, len(data))]

while abs(error - previous_error) > 0.1 or iter > 0:
    iter -= 1
    counter += 1
    # Recomputing
    for i in range(0, len(data)):
        distance = 11111111111
        for j in range(0, K):
            temp_dist = 0
            for k in range(0, len(data[0])):
                temp_dist += (data[i][k] - mean[j][k]) ** 2
            if temp_dist < distance:
				count_class[C.get(i)] -= 1
                C[i] = j
				count_class[C.get(i)] += 1
                distance = temp_dist
                variance[i] = distance
    mean = []
    for i in range(0, K):
        mean.append([0 for j in range(0, len(data[0]))])

    for i in range(0, len(data)):
        for j in range(0, len(data[0])):
            mean[C.get(i)][j] += data[i][j]

    for i in range(0, len(mean)):
        for j in range(0, len(data[0])):
            mean[i][j] /= count_class[i]

    # Compute objective
    previous_error = error
    temp_error = 0
    for i in range(0, len(variance)):
        temp_error += variance[i]

    error = temp_error
    print(error)

for i in range(0, len(data)):
    print(C.get(i), i)
print(counter)
