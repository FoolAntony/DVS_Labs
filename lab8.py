import math

import cv2
import numpy as np


def event_frame(x_list, y_list, polarity_list, image_shape_width, image_shape_height):
    image = np.ones((image_shape_height, image_shape_width))
    image = image * 127
    image = image.astype(np.uint8)
    for i in range(len(polarity_list)):
        if polarity_list[i] == 1:
            image[y_list[i]][x_list[i]] = 255
        elif polarity_list[i] == -1:
            image[y_list[i]][x_list[i]] = 0
    return image


def ex1():
    img = cv2.imread("images/frame_00000022.png", cv2.IMREAD_GRAYSCALE)
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()
    # Change thresholds
    params.minThreshold = 10
    params.maxThreshold = 200
    # Filter
    params.filterByArea = True
    params.minArea = 100
    params.filterByCircularity = False
    params.filterByConvexity = False
    ver = (cv2.__version__).split('.')
    if int(ver[0]) < 3:
        detector = cv2.SimpleBlobDetector(params)
    else:
        detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(img)
    res_img = cv2.drawKeypoints(img, keypoints, np.array([]), (0, 0, 255), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    objects = []
    for keypoint in keypoints:
        objects.append([int(keypoint.pt[0]), int(keypoint.pt[1]), int(keypoint.size)])
    print(objects)
    cv2.imshow("result", res_img)
    cv2.waitKey()

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
            if float(event[0]) >= 1.0:
                if (float(event[0]) <= 5.0):
                    timestamps.append(float(event[0]))
                    x_pos.append(int(event[1]))
                    y_pos.append(int(event[2]))
                    if int(event[3]) == 0:
                        polarity.append(-1)
                    else:
                        polarity.append(1)

        tau = 0.01
        x_s = []
        y_s = []
        polarity_s = []
        timestamps_s = []
        pause_time = 0
        start_time = 0
        for i in range(len(polarity)):
            ev = [x_pos[i], y_pos[i]]
            distance = math.dist([objects[0][0], objects[0][1]], ev)
            object_diameter = objects[0][2]
            obj_index = 0
            for index in range(len(objects)):
                obj = [objects[index][0], objects[index][1]]
                eq_dist = math.dist(obj, ev)
                if eq_dist < distance:
                    distance = eq_dist
                    object_diameter = objects[index][2]
                    obj_index = index
            if object_diameter/2 > distance > 0:
                objects[obj_index][0] = objects[obj_index][0] + (x_pos[i] - objects[obj_index][0]) / 2
                objects[obj_index][1] = objects[obj_index][1] + (y_pos[i] - objects[obj_index][1]) / 2

            if (timestamps[i] - start_time) < tau:
                x_s.append(x_pos[i + pause_time])
                y_s.append(y_pos[i + pause_time])
                timestamps_s.append(timestamps[i + pause_time])
                polarity_s.append(polarity[i + pause_time])
            else:
                im = event_frame(x_s, y_s, polarity_s, image_width, image_height)
                for obj in objects:
                    im = cv2.circle(im, (int(obj[0]), int(obj[1])), obj[2], (0, 0, 255))
                cv2.imshow('image', im)
                cv2.waitKey()
                x_s = []
                y_s = []
                polarity_s = []
                timestamps_s = []
                start_time = timestamps[i]


if __name__ == "__main__":
    ex1()
