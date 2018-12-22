import sys

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

gini_values = [0 for i in data[0]]
split_values = [0 for i in data[0]]
rows = len(data)

#finding minimum and maximum in each column:
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


#calculating gini for each column:
for i in range(0, len(data[0])):
    j = min_values[i]
    temp_gini = 0
    while(j < max_values[i] + 1):
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
        j += 0.5

gini = gini_values[0]
split = split_values[0]
column = 0

for i in range(0, len(gini_values)):
    if(gini > gini_values[i]):
        gini = gini_values[i]
        split = split_values[i]
        column = i

print("column_index[starting from 0]=", column, "split=", split)