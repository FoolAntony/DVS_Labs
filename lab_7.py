import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fmin


def contrast(params, xs, ys, ts, ps, image_width, image_height):
    t_max = max(ts)
    h_image = np.zeros((image_height, image_width), dtype=int)
    for i in range(len(xs)):
        x_wraped = xs[i] - (ts[i] - t_max) * params[0] * 1000000 #TODO calculate transformed X based on speed params[0]
        y_wraped = ys[i] - (ts[i] - t_max) * params[1] * 1000000 #TODO calculate transformed Y based on speed params[1]
        if x_wraped < image_width and y_wraped < image_height: #TODO transformed X and Y are inside the image_shape
            h_image[int(y_wraped), int(x_wraped)] += 1
    value = -1 * np.var(h_image)
    return value


def h_matrix(params, xs, ys, ts, ps, image_width, image_height):
    t_max = max(ts)
    h_image = np.zeros((image_height, image_width), dtype=int)
    normalizedImg = np.zeros((image_height, image_width))
    for i in range(len(xs)):
        x_wraped = xs[i] - (ts[i] - t_max) * params[0] * 1000000 #TODO calculate transformed X based on speed params[0]
        y_wraped = ys[i] - (ts[i] - t_max) * params[1] * 1000000 #TODO calculate transformed Y based on speed params[1]
        if x_wraped < image_width and y_wraped < image_height: #TODO transformed X and Y are inside the image_shape
            h_image[int(y_wraped), int(x_wraped)] += 1
        normalizedImg = cv2.normalize(h_image, normalizedImg, 0, 255, cv2.NORM_MINMAX)
    return normalizedImg


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


def main():
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

        tau = 0.1
        x_s = []
        y_s = []
        polarity_s = []
        timestamps_s = []
        pause_time = 0
        start_time = 1
        for i in range(len(polarity)):
            if (timestamps[i] - start_time) < tau:
                x_s.append(x_pos[i + pause_time])
                y_s.append(y_pos[i + pause_time])
                timestamps_s.append(timestamps[i + pause_time])
                polarity_s.append(polarity[i + pause_time])
            else:
                args = (x_s, y_s, timestamps_s, polarity_s, image_width, image_height)
                im = event_frame(x_s, y_s, polarity_s, image_width, image_height)
                argmax = fmin(contrast, (0, 0), args=args, disp=False)
                print(argmax * 1000000)
                cv2.imshow('image', im)
                cv2.waitKey()
                im_new = h_matrix(argmax, x_s, y_s, timestamps_s, polarity_s, image_width, image_height)
                im_new = im_new.astype(np.uint8)
                cv2.imshow('High Contrast', im_new)
                cv2.waitKey()
                x_s = []
                y_s = []
                polarity_s = []
                timestamps_s = []
                start_time = timestamps[i]


if __name__ == '__main__':
    main()
# Speed should be in px/tau, since we are tracking distance (in pixels) for an amount of time in a frame