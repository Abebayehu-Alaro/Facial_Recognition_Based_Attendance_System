# -*- coding: utf-8 -*-

#!/usr/bin/env python

"""Face recognition module using Tensorflow and Keras.

In this module we train a convolutional neural network
to be able to predict or recognize faces.
"""

__author__ = "abi_alaro"

import numpy as np

# Config
from mtcnn_detector import MTCnnDetector
from vggModelFinal import VggModel
import constant


#Face detector
flag=True
if flag:
    face_detector = MTCnnDetector(constant.CELEBRITY_VGG_PATH, False, False)
else:
#Model
    vgg = VggModel()
    vgg.train(20,4)
#vgg.evaluate()
