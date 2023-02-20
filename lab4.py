import os
import numpy as np
import cv2

owd = os.getcwd()


def read_dataset(filename):
    f = open(filename, 'rb')
    raw_data = np.fromfile(f, dtype=np.uint8)
    f.close()
    raw_data = np.uint32(raw_data)
    all_y = raw_data[1::5]
    all_x = raw_data[0::5]
    all_p = (raw_data[2::5] & 128) >> 7 	# bit 7
    all_ts = ((raw_data[2::5] & 127) << 16) | (raw_data[3::5] << 8) | (raw_data[4::5])
    time_increment = 2 ** 13
    overflow_indices = np.where(all_y == 240)[0]
    for overflow_index in overflow_indices:
        all_ts[overflow_index:] += time_increment
    td_indices = np.where(all_y != 240)[0]
    x = all_x[td_indices]
    w = x.max() + 1
    y = all_y[td_indices]
    h = y.max() + 1
    ts = all_ts[td_indices]
    p = all_p[td_indices]
    return ts, x, y, p, h, w


def event_frame(x_list, y_list, polarity_list, image_shape_width, image_shape_height):
    image = np.ones((image_shape_width, image_shape_height))
    image = image * 127
    image = image.astype(np.uint8)
    for i in range(len(polarity_list)):
        if polarity_list[i] == 1:
            image[x_list[i]][y_list[i]] = 255
        else:
            image[x_list[i]][y_list[i]] = 0
    return image


def image_generate(timestamps_x, x_pos, y_pos, polarity, height, width, file_path, filename):
    tau = 50000  # 50ms
    x_s = []
    y_s = []
    polarity_s = []
    count_images = 0
    start = 0
    dir_to = 'frame_data' + file_path[8:]
    for i in range(len(polarity)):
        if (timestamps_x[i] - start) < tau:
            x_s.append(x_pos[i])
            y_s.append(y_pos[i])
            # timestamps_s.append(timestamps_x[i])
            polarity_s.append(polarity[i])
        else:
            count_images += 1
            im = event_frame(x_s, y_s, polarity_s, width, height)
            os.chdir(os.path.normpath(dir_to))
            cv2.imwrite('image_' + filename[:4] + '_' + str(count_images) + '.png', im)
            os.chdir(owd)
            start = timestamps_x[i]
            x_s = []
            y_s = []
            polarity_s = []


main_dir = 'raw_data'
count = 0
total_events = 0
files_amount = 0


for root, dirs, files in os.walk(main_dir):
    for file in files:
        # count += 1
        timestamps, xaddr, yaddr, pol, h, w = read_dataset(os.path.join(root, file))
        print(root)
        # print("Last timestamp: ", timestamps[-1])
        image_generate(timestamps, xaddr, yaddr, pol, h, w, root, file)
        # total_events += len(timestamps)
        # print(file.path)
        # print("In ", d, " there are ", count, "\n")
#     files_amount += count
#     count = 0
# average = total_events/files_amount
#
# print("Average of events: ", int(average))

print("Finished successfully!")
