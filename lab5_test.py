import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt


def main():
    train_ds = tf.keras.utils.image_dataset_from_directory('frame_data/Train', batch_size=32, image_size=(34, 34))
    model = tf.keras.models.load_model('network')
    model.evaluate(x=train_ds, batch_size=32)
    image = cv2.imread("frame_data/Test/9/image_0033_1.png")
    image_to_pred = image.reshape(1, 34, 34, 3)
    predict = model.predict(image_to_pred, batch_size=1)
    for x in range(10):
        value = float(predict[0][x])
        print("The probability that the number is " + str(x) + " equals " + str(value*100))
    cv2.imshow("image", image)
    cv2.waitKey()


if __name__ == "__main__":
    main()
