import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


timestamps = []
x_pos = []
y_pos = []
polarity = []
with open('tennis2.txt', 'r') as file:
    data = file.read()
    split_data = data.split('\n')
    for i in split_data:
        event = list()
        event = i.split(' ')
        if float(event[0]) <= 1.0:
          timestamps.append(float(event[0]))
          x_pos.append(int(event[1]))
          y_pos.append(int(event[2]))
          polarity.append(int(event[3]))
    print('Total of events', len(timestamps))
    print('First timestamp', timestamps[0])
    print('Last timestamp', timestamps[-1])


    min = 364
    max = 0
    for i in x_pos:
        if x_pos[i] > max:
            max = x_pos[i]
        if x_pos[i] < min:
            min = x_pos[i]
    print('x coordinate max and min: ', max, min)

    max = 0
    min = 260
    for j in y_pos:
        if y_pos[j] < min:
            min = y_pos[j]
        if y_pos[j] > max:
            max = y_pos[j]
    print('y coordinates max and min:', max, min)

    pos = 0
    neg = 0
    for i in polarity:
        if i < 1:
            neg += 1
        else:
            pos += 1
    print('Positive polarity:', pos)
    print('Negative polarity:', neg)


# dividing into positive and negative
    pos_timestamps = list()
    pos_x = list()
    neg_x = list()
    pos_y = list()
    neg_timestamps = list()
    neg_y = list()
    # for i in range(8000):
    #     #for the first task, len(polatiry) has been used
    #     #for the second task, range(8000) has been used
    #     if polarity[i] == 1:
    #         pos_timestamps.append(timestamps[i])
    #         pos_x.append(x_pos[i])
    #         pos_y.append(y_pos[i])
    #     else:
    #         neg_timestamps.append(timestamps[i])
    #         neg_x.append(x_pos[i])
    #         neg_y.append(y_pos[i])

    # timestamps from 0.5 to 1.0
    for i in range(len(polarity)):
        if timestamps[i] >= 0.99:
            if polarity[i] == 1:
                pos_timestamps.append(timestamps[i])
                pos_x.append(x_pos[i])
                pos_y.append(y_pos[i])
            else:
                neg_timestamps.append(timestamps[i])
                neg_x.append(x_pos[i])
                neg_y.append(y_pos[i])


    print("Number of new events: ", len(pos_y) + len(neg_y))

# figure
    ax = plt.axes(projection = '3d')

#creation
    ax.scatter3D(pos_x, pos_y, pos_timestamps, color = "blue", marker ='^')
    ax.scatter3D(neg_x, neg_y, neg_timestamps, color = "red", marker = 'v')
    plt.title("DVS Lav 1")
    ax.set_xlabel('X-axis', fontweight = 'bold')
    ax.set_ylabel('Y-axis',fontweight = 'bold')
    ax.set_zlabel('Timestamps',fontweight = 'bold')
    ax.legend(['positive', 'negative'])
    #ax.view_init(60, 0, -45)

    plt.show()

    # task 1.2.3(a)
    # The length of sequence is 59.798386001 seconds

    # task 1.2.3(c)
    # according to my obsevations, amount of event before 0.5 timestamps is less than after, which means it depends on
    # if there are any actions happens. More actions happenes next to dvs = more events generated

    # task 1.2.3(d)
    # pos/neg polarity means

    # task 1.2.3(e)
    # the direction of movement of objects is forward up to 1.0 timestamp (moving along the x-axis)