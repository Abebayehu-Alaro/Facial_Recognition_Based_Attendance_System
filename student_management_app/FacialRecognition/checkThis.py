# Face detector
from mtcnn_detector import MTCnnDetector
#from util import constant
face_detector = MTCnnDetector("E:/Final Project/code/FR/datasetFinal/sisay_belete/sis_photo14.jpg")
resized_faces = face_detector.process_image(plot=False)
