import cv2
import numpy as np
import os
import sys
import tensorflow as tf

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    """
    ### print used filters #################################
    # Zugriff auf den Conv2D-Layer
    conv_layer = model.layers[0]

    # Zugriff auf die Gewichtsmatrizen (Filter) des Conv2D-Layers
    filters = conv_layer.get_weights()[0]

    # Visualisierung der Gewichtsmatrizen
    plt.figure(figsize=(8, 8))
    for i in range(filters.shape[3]):
        plt.subplot(8, 8, i + 1)  # Anpassen je nach Anzahl der Filter
        plt.imshow(filters[:, :, 0, i], cmap='gray')
        plt.axis('off')

    plt.show()
    ########################################################
    """

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """

    print("LOADING DATA ...")
    lst_images = []
    lst_labels = []
    i = 0
    for subdir in range(NUM_CATEGORIES):
        path_subdir = os.path.join(data_dir, str(subdir))
        for file in os.listdir(path_subdir):
            fullpath = os.path.join(path_subdir,file)
            im_array = cv2.imread(fullpath)
            im_array = cv2.resize(im_array, (IMG_WIDTH, IMG_HEIGHT))
            # print(im_array.shape)
            lst_images.append(im_array)
            lst_labels.append(int(subdir))

        print(f"FINISHED READING SUBDIRECTORY {i+1} out of {NUM_CATEGORIES}.")
        i += 1
    # print(im_array)
    # print(type(im_array))
    return (lst_images, lst_labels)

    # raise NotImplementedError


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """

    model = tf.keras.Sequential([

            tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_HEIGHT,IMG_WIDTH, 3)),
            tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
            tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_HEIGHT,IMG_WIDTH, 3)),
            tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
            # tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_HEIGHT,IMG_WIDTH, 3)),
            # tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
            # tf.keras.layers.Conv2D(32, (3,3), activation="relu", input_shape=(IMG_HEIGHT,IMG_WIDTH, 3)),
            # tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(256, activation="relu"),
            tf.keras.layers.Dense(256, activation="relu"),
            tf.keras.layers.Dense(256, activation="relu"),
            # tf.keras.layers.Dense(256, activation="relu"),
            # tf.keras.layers.Dense(256, activation="relu"),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")      
    ])


    # Train neural network
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

    # raise NotImplementedError


if __name__ == "__main__":
    main()
