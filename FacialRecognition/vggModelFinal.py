# -*- coding: utf-8 -*-
import os

import keras
# from tensorflow import keras
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions

from numpy import expand_dims
import numpy as np

from tensorflow.python.keras import Input
from tensorflow.python.keras.applications.vgg16 import VGG16
from tensorflow.python.keras.layers import MaxPooling2D, Dense, Flatten, Convolution2D
from tensorflow.python.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
import constant
from common import Common


class VggModel:

    def __init__(self):

        self.init_model()
        opt = keras.optimizers.Adam(learning_rate=0.001)
        self.vgg.compile(loss=keras.losses.binary_crossentropy,
                         optimizer=opt,
                         metrics=[constant.METRIC_ACCURACY])

    def init_model(self):

        base_model = VGG16(weights=constant.IMAGENET, include_top=False,
                           input_tensor=Input(shape=(constant.IMG_WIDTH,
                                                     constant.IMG_HEIGHT, 3)), pooling='max', classes=17)
        # base_model.summary()

        for layer in base_model.layers:
            layer.trainable = False

        x = base_model.get_layer('block5_pool').output
        # Stacking a new simple convolutional network on top of it
        x = Convolution2D(64, 3)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)
        x = Flatten()(x)
        x = Dense(constant.NUMBER_FULLY_CONNECTED, activation=constant.RELU_ACTIVATION_FUNCTION)(x)
        x = Dense(17, activation=constant.SOFTMAX_ACTIVATION_FUNCTION)(x)

        self.vgg = Model(inputs=base_model.input, outputs=x)
        # self.vgg.summary()

    def get_model(self):
        saved_model = load_model("vgg16_1.h5")
        return saved_model

    def train(self, num_epochs=10, num_batchs=10):

        datagen = ImageDataGenerator(rescale=1. / 255,
                                     shear_range=0.4,
                                     zoom_range=0.2,
                                     rotation_range=50,
                                     width_shift_range=0.2,
                                     height_shift_range=0.2,
                                     horizontal_flip=True,
                                     fill_mode='nearest')
        #
        traindata = datagen.flow_from_directory(
            directory="E:/Final Project/Implementation/FinalProject/dataset/yalefaces/training_set",
            target_size=(constant.IMG_WIDTH,
                         constant.IMG_HEIGHT))

        testdata = datagen.flow_from_directory(
            directory="E:/Final Project/Implementation/FinalProject/dataset/yalefaces/test_set",
            target_size=(constant.IMG_WIDTH,
                         constant.IMG_HEIGHT))

        # checkpoint = ModelCheckpoint("vgg16_1.h5", monitor='val_accuracy', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)
        checkpoint = ModelCheckpoint("vgg16_1.h5", monitor=constant.METRIC_ACCURACY, verbose=1, save_best_only=True,
                                     save_weights_only=False, mode='auto', period=1)
        # early = EarlyStopping(monitor='val_accuracy', min_delta=0, patience=20, verbose=1, mode='auto')
        early = EarlyStopping(monitor=constant.METRIC_ACCURACY, min_delta=0, patience=20, verbose=1, mode='auto')
        self.vgg.fit_generator(steps_per_epoch=num_batchs, generator=traindata, validation_data=testdata,
                               validation_steps=10, epochs=num_epochs, callbacks=[checkpoint, early])

    def __process_img(self, img):
        # img = image.load_img(img_path,target_size=(constant.IMG_WIDTH,
        # constant.IMG_HEIGHT))
        img = image.img_to_array(img)
        # img = Common.reshape_from_img(img)
        # img = Common.reshape_data(img)

        # return preprocess_input(img)

        return preprocess_input(expand_dims(img, axis=0))

    #        # load an image from file
    #        image = load_img(img_path, target_size=(constant.IMG_WIDTH, constant.IMG_HEIGHT))
    #        # convert the image pixels to a numpy array
    #        image = img_to_array(image)
    #        # reshape data for the model
    #        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    #        # prepare the image for the VGG model
    #        image = preprocess_input(image)
    #        return image
    def predict(self, img):
        pixels = self.__process_img(img)
        saved_model = self.get_model()
        output = saved_model.predict(pixels)
        self.print_predication_result(output)

    def print_predication_result(self, output):
        AllClassNames = self.getAllClassNames()
        num_of_classes = len(AllClassNames)
        DictOfClasses = {i: AllClassNames[i] for i in range(0, len(AllClassNames))}
        temp = 0
        index = 0
        for i in range(0, num_of_classes):
            if output[0][i] > temp:
                temp = output[0][i]
                index = i
        class_value = self.id_class_name(index, DictOfClasses)
        print(class_value)

    #

    def id_class_name(self, class_id, classes):
        """
        Returns name of the class as per the given id
        
        Args:
            class_id(int): Number of the class.
            classes(dict): dictinary of all the classes in given dataset.
            
        returns:
            Name of the Class.
        """
        for key, value in classes.items():
            if class_id == key:
                return value

    def getAllClassNames(self):
        """
            Returns list of all class names in given Training/Test dir path.
        """
        dir_path = "E:/Final Project/Implementation/FinalProject/dataset/yalefaces/training_set"
        return os.listdir(dir_path)

#    def evaluate(self):
#        super(VggModel, self).evaluate()

# model =  VggModel()
##model.train()
# img_path = "dataset/test_set/dogs/dog.4019.jpg"
# output = model.predict(img_path)
###label = decode_predictions(output)
###label = label[0][0]
#### print the classification
###print('%s (%.2f%%)' % (label[1], label[2]*100))
###print(label)
# if output[0][0] > output[0][1]:
#    print("cat")
# else:
#    print('dog')
