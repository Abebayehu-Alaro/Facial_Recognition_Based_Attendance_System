# -*- coding: utf-8 -*-
import os

import keras
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
import matplotlib.pyplot as plt
from numpy import expand_dims
import numpy as np

from tensorflow.python.keras import Input
from tensorflow.python.keras.applications.vgg16 import VGG16
from tensorflow.python.keras.layers import MaxPooling2D, Dense, Flatten, Convolution2D
from tensorflow.python.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
from . import constant


# from student_management_app.models import MLModel

class VggModel:
    dir_path_train = "E:/Final Project/Implementation/Dataset_Final_Project/Training_Set"
    dir_path_test = "E:/Final Project/Implementation/Dataset_Final_Project/Testing_Set"
    number_of_samples = 0
    all_class_names = os.listdir(dir_path_train)
    number_of_classes = len(all_class_names)

    def __init__(self, flag=True):

        if flag:
            self.init_model()
            opt = keras.optimizers.Adam(learning_rate=0.001)
            self.vgg.compile(loss=keras.losses.binary_crossentropy,
                             optimizer=opt,
                             metrics=[constant.METRIC_ACCURACY])

    def init_model(self):

        base_model = VGG16(weights=constant.IMAGENET, include_top=False,
                           input_tensor=Input(shape=(constant.IMG_WIDTH,
                                                     constant.IMG_HEIGHT, 3)), pooling='max',
                           classes=self.number_of_classes)
        # base_model.summary()

        for layer in base_model.layers:
            layer.trainable = False

        x = base_model.get_layer('block5_pool').output
        # Stacking a new simple convolutional network on top of it
        x = Convolution2D(64, 3)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)
        x = Flatten()(x)
        x = Dense(constant.NUMBER_FULLY_CONNECTED, activation=constant.RELU_ACTIVATION_FUNCTION)(x)
        x = Dense(self.number_of_classes, activation=constant.SOFTMAX_ACTIVATION_FUNCTION)(x)

        self.vgg = Model(inputs=base_model.input, outputs=x)
        # self.vgg.summary()

    def get_model(self):  # , model_weight_url):
        saved_model = load_model("student_management_app/FacialRecognition/FinalTrainedModel/vgg16.h5")
        # saved_model = load_model(model_weight_url)
        return saved_model

    def train(self, num_epochs=10, num_batches=10, flag=True):

        datagen = ImageDataGenerator(rescale=1. / 255,
                                     shear_range=0.4,
                                     zoom_range=0.2,
                                     rotation_range=50,
                                     width_shift_range=0.2,
                                     height_shift_range=0.2,
                                     horizontal_flip=True,
                                     fill_mode='nearest')

        traindata = datagen.flow_from_directory(
            self.dir_path_train,
            target_size=(constant.IMG_WIDTH,
                         constant.IMG_HEIGHT))
        self.number_of_samples = traindata.samples
        if flag:
            testdata = datagen.flow_from_directory(
                self.dir_path_test,
                target_size=(constant.IMG_WIDTH,
                             constant.IMG_HEIGHT))

            number_of_samples_test = testdata.samples

            # Configure the dataset for performance
            # AUTOTUNE = tf.data.AUTOTUNE

            # train_data = traindata.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
            # test_data = testdata.cache().prefetch(buffer_size=AUTOTUNE)

            checkpoint = ModelCheckpoint("student_management_app/FacialRecognition/FinalTrainedModel/vgg16.h5",
                                         monitor=constant.METRIC_ACCURACY, verbose=1, save_best_only=True,
                                         save_weights_only=False, mode='auto', period=1)
            early = EarlyStopping(monitor=constant.METRIC_ACCURACY, min_delta=0, patience=20, verbose=1, mode='auto')
            self.vgg.fit_generator(steps_per_epoch=self.number_of_samples // num_batches, generator=traindata,
                                   validation_data=testdata,
                                   validation_steps=number_of_samples_test // num_batches, epochs=num_epochs,
                                   callbacks=[checkpoint, early])
            #self.evaluating_the_model(testdata)
            # self.evaluate()
            # self.plot_accuracy_loss(num_epochs)

    def __process_img(self, img):

        img = image.img_to_array(img)

        return preprocess_input(expand_dims(img, axis=0))

    def predict(self, img):  # model_weight_url):
        pixels = self.__process_img(img)
        # saved_model = self.get_model(model_weight_url)
        saved_model = self.get_model()
        output = saved_model.predict(pixels)
        # output = saved_model.predict(pixels)
        # return output
        return self.print_predication_result(output)

    def print_predication_result(self, output):

        dict_of_classes = {i: self.all_class_names[i] for i in range(0, self.number_of_classes)}
        temp = 0
        index = 0
        flag = 0
        for i in range(0, self.number_of_classes):
            if output[0][i] > temp:
                temp = output[0][i]
                flag = temp
                index = i
        if round(float(flag), 2) == round(float(1.0000), 2):
            class_value = self.id_class_name(index, dict_of_classes)
            return class_value
        else:
            return ""

    def id_class_name(self, class_id, classes):
        for key, value in classes.items():
            if class_id == key:
                return value

    def evaluate(self):
        score = self.get_model().evaluate(verbose=0)
        print("%s: %.2f%%" % (self.get_model().metrics_names[1], score[1] * 100))

    def get_number_class_samples(self):
        return self.number_of_classes, self.number_of_samples

    def plot_accuracy_loss(self, epochs):
        # loss
        acc = self.get_model().history['accuracy']
        val_acc = self.get_model().history['val_accuracy']

        loss = self.get_model().history['loss']
        val_loss = self.get_model().history['val_loss']

        epochs_range = range(epochs)

        plt.figure(figsize=(8, 8))
        plt.subplot(1, 2, 1)
        plt.plot(epochs_range, acc, label='Training Accuracy')
        plt.plot(epochs_range, val_acc, label='Validation Accuracy')
        plt.legend(loc='lower right')
        plt.title('Training and Validation Accuracy')

        plt.subplot(1, 2, 2)
        plt.plot(epochs_range, loss, label='Training Loss')
        plt.plot(epochs_range, val_loss, label='Validation Loss')
        plt.legend(loc='upper right')
        plt.title('Training and Validation Loss')
        plt.show()

    # Evaluating the model on test datasets
    def evaluating_the_model(self, test_generator):
        self.get_model().evaluate_generator(test_generator)
