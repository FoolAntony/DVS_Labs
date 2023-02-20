import numpy as np
import pandas as pd
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

# Verifying my conclusions
timestamps = []
x_pos = []
y_pos = []
polarity = []
with open('events.txt', 'r') as file:
    data = file.read()
    split_data = data.split('\n')
    for i in split_data:
        event = list()
        event = i.split(' ')
        if float(event[0]) >= 0.5:
            if (float(event[0]) <= 1.0):
                timestamps.append(float(event[0]))
                x_pos.append(int(event[1]))
                y_pos.append(int(event[2]))
                if int(event[3]) == 0:
                    polarity.append(-1)
                else:
                    polarity.append(1)


initial_timestamp = timestamps[0]
avg_timestamp = []
avg_x = []
avg_y = []
sum_timestamp = 0
sum_x = 0
sum_y = 0
count = 0
for i in range(len(timestamps)):
    if(timestamps[i] <= initial_timestamp + (0.001) ):
        sum_timestamp += timestamps[i]
        sum_x += x_pos[i]
        sum_y += y_pos[i]
        count += 1
    else:
        initial_timestamp = timestamps[i]
        avg_timestamp.append(float(sum_timestamp/count))
        avg_x.append(sum_x/count)
        avg_y.append(sum_y/count)
        sum_timestamp = timestamps[i]
        sum_x = x_pos[i]
        sum_y = y_pos[i]
        count = 1





events = pd.DataFrame(list(zip(avg_x, avg_y, avg_timestamp)),

               columns =['avg_x', 'avg_y', 'avg_timestamp'])

events = events.head(500)

fig = plt.figure(figsize = (10, 7))
axes = fig.add_subplot(projection = "3d")


axes.scatter(events.avg_x, events.avg_y, events.avg_timestamp, c="green")

print("The difference between first and last avg x: ", events.avg_x.iloc[-1] - events.iloc[0])



axes.set_title("Average values of pixel connrdinate with timestamp between 0.5 and 1")
axes.set_xlabel('average x-coordinate', fontweight ='bold')
axes.set_ylabel('average y-coordinate', fontweight ='bold')
axes.set_zlabel('average timestamp', fontweight ='bold')


plt.show()
