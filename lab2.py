import cv2 as opencv
import numpy as np


def event_frame(x_list, y_list, polarity_list, image_shape_width, image_shape_height):
    image = np.ones((image_shape_width, image_shape_height))
    image = image * 127
    image = image.astype(np.uint8)
    for i in range(len(polarity_list)):
        if polarity_list[i] == 1:
            image[x_list[i]][y_list[i]] = 255
        elif polarity_list[i] == -1:
            image[x_list[i]][y_list[i]] = 0
    return image


def exponential_decay(timestamps_list, x_list, y_list, polarity_list, t, image_shape_width, image_shape_height):
    img = np.zeros((image_shape_width, image_shape_height))
    normalizedImg = np.zeros((image_shape_width, image_shape_height))
    timestamp_max = timestamps_list[-1]
    for i in range(len(polarity_list)):
        if timestamps_list[i] <= timestamp_max:
            f = (timestamps_list[i] - timestamp_max) / t
            img[x_list[i]][y_list[i]] = 255 * np.exp(f)
    normalizedImg = opencv.normalize(img, normalizedImg, 0, 255, opencv.NORM_MINMAX)
    normalizedImg = normalizedImg.astype(np.uint8)
    return normalizedImg


def event_frequency(x_list, y_list, polarity_list, image_shape_width, image_shape_height):
    img = np.zeros((image_shape_width, image_shape_height))
    normalizedImg = np.zeros((image_shape_width, image_shape_height))
    for i in range(len(polarity_list)):
        img[x_list[i]][y_list[i]] += polarity_list[i]
    img = 255 * (1 + np.exp(-img / 2))
    normalizedImg = opencv.normalize(img, normalizedImg, 0, 255, opencv.NORM_MINMAX)
    normalizedImg = normalizedImg.astype(np.uint8)
    return normalizedImg



image_width = 240
image_height = 180
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
        if float(event[0]) > 1.0:
            if (float(event[0]) < 2.0):
                timestamps.append(float(event[0]))
                x_pos.append(int(event[1]))
                y_pos.append(int(event[2]))
                if int(event[3]) == 0:
                    polarity.append(-1)
                else:
                    polarity.append(1)
    print('Total of events', len(timestamps))
    print('First timestamp', timestamps[0])
    print('Last timestamp', timestamps[-1])
    # for i in range(30):
    #     print('Polarity', polarity[i], type(polarity[i]))

    tau = 0.001  # 10ms
    # Task 2.1.11:
    #
    # The aggregation time "tua" affect the generated event frames in such a way, that for shorter times there are more
    # frames generated, but it is hard to observe any shape. It happens because for smaller time limits there are lack
    # of event data which could produce assemble into a normal picture. However, we can see more detailed sequence of
    # event changing.
    #
    # In case of greater aggregation time, it is opposite situation: the amount of events per frame is larger, so we
    # can observe better object shape generation. But there is another problem: for some of these frames, the time
    # limit is so large that it cannot catch any events, and that puts us in the situation when we cannot see anything
    # on the frame. So the time of 10ms gives us the compromise between event changing demonstration and object shape
    # recognition.

    x_s = []
    y_s = []
    polarity_s = []
    timestamps_s = []
    pause_time = 0
    start_time = 0

    for i in range(len(polarity)):
        if (timestamps[i] - start_time) < tau:
            x_s.append(x_pos[i + pause_time])
            y_s.append(y_pos[i + pause_time])
            timestamps_s.append(timestamps[i + pause_time])
            polarity_s.append(polarity[i + pause_time])
        else:
            # im = event_frame(x_s, y_s, polarity_s, image_width, image_height)
            # im = exponential_decay(timestamps_s, x_s, y_s, polarity_s, tau, image_width, image_height)
            im = event_frequency(x_s, y_s, polarity_s, image_width, image_height)
            opencv.imshow('image', im)
            opencv.waitKey()
            x_s = []
            y_s = []
            polarity_s = []
            timestamps_s = []
            start_time = timestamps[i]
