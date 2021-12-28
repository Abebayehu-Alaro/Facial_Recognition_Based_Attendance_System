# -*- coding: utf-8 -*-

# !/usr/bin/env python

"""Face recognition module using Tensorflow and Keras.

In this module we train a convolutional neural network
to be able to predict or recognize faces.
"""

__author__ = "abi_alaro"

import numpy as np

# Config
from .mtcnn_detector import MTCnnDetector
from .vggModelFinal import VggModel


# import constant


class MainClass:
    @staticmethod
    def make_predication(img_path): #, model_weight_url):

       # answer = MTCnnDetector.control_all(img_path, False, False)
       #  return MTCnnDetector.control_all(img_path, model_weight_url, False, False)
        return MTCnnDetector.control_all(img_path, False, False)

    @staticmethod
    def train_model(epoch=1, batch=4):
        vgg = VggModel()
        vgg.train(epoch, batch)

    @staticmethod
    def get_number_of_class_samples():
        vgg = VggModel(flag=False)
        vgg.train(flag=False)
        classes, samples = vgg.get_number_class_samples()
        return classes, samples

