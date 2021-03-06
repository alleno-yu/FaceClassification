import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import pickle
import tensorflow as tf
from sklearn.model_selection import train_test_split
# this is data preprocessing function, takes three arguments(img sizem, img path and csv file path)
# it runs over all imgs under img_path root and convert into array using cv2.imread function
# it this function returns 6 datasets arrays, x and y for training, val and test.
# the data set is split into 70% for training, 20% for validation and 10% for testing
# the array data is already normalized, results are between 0 and 1
def B2_data_preprocessing(IMG_SIZE, img_path, label_path):
    training_data = []

    labels_file = open(label_path, 'r')
    lines = labels_file.readlines()
    facial_labels = {line.split("\t")[3].split("\n")[0]: int(line.split("\t")[1]) for line in lines[1:]}

    for img in os.listdir(img_path):  # for each image in the path
        class_num = facial_labels[img]
        try:
            img_array = cv2.imread(os.path.join(img_path, img),cv2.IMREAD_GRAYSCALE)
            new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
            training_data.append([new_array, class_num])
        except Exception as e:
            pass
    X = []
    y = []

    for features, label in training_data:
        X.append(features)
        y.append(label)

    X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    y = np.array(y)

    X = tf.keras.utils.normalize(X, axis=1)

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.222222, random_state=0)

    return x_train, x_test, y_train, y_test, x_val, y_val

if __name__ == "__main__":
    # path for img folder and csv file
    # these paths are relative path, pls put cartoon_set folder under Datasets folder
    img_path = r"../Datasets/cartoon_set/img"
    label_path = r"../Datasets/cartoon_set/labels.csv"

    #call data processing functions, imgs are resized into 70x70
    B2_x_train, B2_x_test, B2_y_train, B2_y_test, B2_x_val, B2_y_val = B2_data_preprocessing(IMG_SIZE=70,
                                                                                             img_path=img_path,
                                                                                             label_path=label_path)
    # use pickle to store splited training dataset and validation dataset
    # this file is either called from main, or run as script to produce pickle file for model training use
    print(B2_x_train.shape)
    pickle_out = open("../Datasets/B2_dataset/x_train.pickle", "wb")
    pickle.dump(B2_x_train, pickle_out)
    pickle_out.close()

    print(B2_x_val.shape)
    pickle_out = open("../Datasets/B2_dataset/x_val.pickle", "wb")
    pickle.dump(B2_x_val, pickle_out)
    pickle_out.close()

    print(B2_y_train.shape)
    pickle_out = open("../Datasets/B2_dataset/y_train.pickle", "wb")
    pickle.dump(B2_y_train, pickle_out)
    pickle_out.close()

    print(B2_y_val.shape)
    pickle_out = open("../Datasets/B2_dataset/y_val.pickle", "wb")
    pickle.dump(B2_y_val, pickle_out)
    pickle_out.close()