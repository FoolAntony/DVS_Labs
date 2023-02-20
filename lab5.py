import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt


def main():

    train_ds = tf.keras.utils.image_dataset_from_directory('frame_data/Train', batch_size=32, image_size=(34, 34))
    val_ds = tf.keras.utils.image_dataset_from_directory('frame_data/Test', batch_size=32, image_size=(34, 34))

    num_classes = 10

    model = tf.keras.Sequential([
        tf.keras.layers.Rescaling(1./255),
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  metrics=['accuracy'],
                  loss=tf.keras.losses.SparseCategoricalCrossentropy())

    history = model.fit(x=train_ds, validation_data=val_ds, epochs=5, batch_size=32)

    model.save('network')

    # list all data in history
    print(history.history.keys())
    # summarize history for accuracy
    plt.figure()
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

# Epoch - iteration over entire dataset, sequence etc.
# Batch size - number of samples per gradient update / full pass of the training algorithm over the entire training set.

# An iteration is one step taken in the gradient descent algorithm towards minimizing
# the loss function using a mini-batch.

# Number of iterations per epochs is the number of passed steps within the whole set. It is the amount of iterations
# passed through the gradient


if __name__ == "__main__":
    main()
