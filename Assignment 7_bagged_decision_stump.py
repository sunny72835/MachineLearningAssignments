import sys
import random

data_file = sys.argv[1]
labels_file = sys.argv[2]

data = []

with open(data_file, "r") as file:
    line = file.readline()
    while line:
        temp = []
        for i in line.split():
            temp.append(float(i))
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


def generate_stump(data, labels):
    gini_values = [0 for i in data[0]]
    split_values = [0 for i in data[0]]
    rows = len(data)

    # finding minimum and maximum in each column:
    min_values = [0 for i in data[0]]
    max_values = [0 for i in data[0]]

    for i in range(0, len(data[0])):
        min = data[0][i]
        max = data[0][i]
        for j in range(0, len(data)):
            if data[j][i] < min:
                min = data[j][i]
            if data[j][i] > max:
                max = data[j][i]
        min_values[i] = min
        max_values[i] = max

    # calculating gini for each column:
    for i in range(0, len(data[0])):
        j = min_values[i]
        temp_gini = 0
        while (j < max_values[i] + 1):
            rp = 0
            rsize = 0
            lp = 0
            lsize = 0
            for k in range(0, len(data)):
                if (data[k][i] < j):
                    lsize += 1
                    if (labels.get(k) == -1):
                        lp += 1
                else:
                    rsize += 1
                    if (labels.get(k) == 1):
                        rp += 1
            if lsize != 0 and rsize != 0:
                temp_gini = (lp / rows) * (1 - (lp / lsize)) + (rp / rows) * (1 - (rp / rsize))
            if lsize == 0 and rsize != 0:
                temp_gini = (rp / rows) * (1 - (rp / rsize))
            if rsize == 0 and lsize != 0:
                temp_gini = (lp / rows) * (1 - (lp / lsize))

            if j == min_values[i]:
                gini_values[i] = temp_gini
                split_values[i] = j

            else:
                if gini_values[i] > temp_gini:
                    gini_values[i] = temp_gini
                    split_values[i] = j
            j += 0.1

    gini = gini_values[0]
    split = split_values[0]
    column = 0

    for i in range(0, len(gini_values)):
        if (gini > gini_values[i]):
            gini = gini_values[i]
            split = split_values[i]
            column = i
    return column, split


#Building training_data set
training_data = []
training_labels = {}
predictions = {}

j = 0
for i in range(0, len(data)):
    if(labels.get(i) != None):
        training_data.append(data[i])
        training_labels[j] = labels.get(i)
        j += 1

for k in range(0, 100):
    # Generate bootstrapped dataset
    bootstrapped_dataset = []
    bootstrapped_labels = {}
    j = 0
    for i in range(0, len(training_data)):
        random_row = random.randint(0, len(training_data) - 1)
        bootstrapped_dataset.append(training_data[random_row])
        bootstrapped_labels[j] = training_labels.get(random_row)
        j += 1

    #Finding stump in bootstrapped_dataset
    column, split = generate_stump(bootstrapped_dataset, bootstrapped_labels)

    #Determine left and right
    zeroes_left = 0
    ones_left = 0
    zeroes_right = 0
    ones_right = 0
    left = 0
    right = 1
    for i in range(0, len(bootstrapped_dataset)):
        if bootstrapped_dataset[i][column] < split:
            if bootstrapped_labels.get(i) < 1:
                zeroes_left += 1
            else:
                ones_left += 1
        else:
            if bootstrapped_labels.get(i) < 1:
                zeroes_right += 1
            else:
                ones_right += 1

    if zeroes_left / ones_left > zeroes_right / ones_right:
        left = 0
        right = 1
    else:
        right = 0
        left = 1

    #Prediction for kth iteration
    for i in range(0, len(data)):
        if labels.get(i) == None:
            if predictions.get(i) == None:
                predictions[i] = []
            if(data[i][column] < split):
                predictions[i].append(left)
            else:
                predictions[i].append(right)
    # print(k, column, split)

# Deciding label by majority:
keys = sorted(predictions.keys())
for i in keys:
    count_0 = 0
    count_1 = 0
    for j in predictions[i]:
        if j == 0:
            count_0 += 1
        else:
            count_1 += 1
 #   print(i, count_0, count_1)
    if count_0 > count_1:
        print("0", i)
    else:
        print("1", i)
