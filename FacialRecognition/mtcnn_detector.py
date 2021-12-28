from PIL import Image
from matplotlib import pyplot
from mtcnn import MTCNN
from numpy import asarray
import numpy as np
from numpy import savetxt
from tensorflow.keras.preprocessing.image import img_to_array
from skimage import io
from PIL import Image as im
import constant
from vggModelFinal import VggModel


class MTCnnDetector:

    def __init__(self, image_path, store_flag=False, plot=False):
        self.detector = MTCNN()
        self.image = io.imread(image_path)
        self.store_flag = store_flag
        self.process_image(plot)

    def process_image(self, plot):
        faces = self.__detect_face();
        resized_face_list = []
        index = 1
        for f in faces:
            extracted_face = self.__extract_face(f)
            resized_face = self.__resize_img_to_face(extracted_face)
            resized_face_list.append(resized_face)
            index = index + 1
            self.select_store_or_predict(resized_face, index)
            # self._save_images_csv(resized_face,index)
            #            image_name = "C:/Users/Hello/FR/photos/nomalizedImages/normalized" + str(index)
            #            resized_face.save(image_name+".jpg")
            if plot:
                self.__plot_face(resized_face)
        return resized_face_list

    def select_store_or_predict(self, face, index):
        if self.store_flag:
            self._save_images_format(face, index)
        else:
            model = VggModel()
            model.predict(face)

    def _save_images_format(self, face, index):
        sample_images_nomalized = []
        sample_images_nomalized = face
        # sample_images_nomalized = np.reshape(sample_images_nomalized, (120, 120)) #Reshape the array into a familiar resoluition
        data = im.fromarray(sample_images_nomalized)  # creating image object of above sample_images_nomalized
        if index < 10:
            image_name = "E:/Final Project/Implementation/FinalProject/dataset/datasetFinal/butera/bute" + str(
                index) + ".jpg"
            data.save(image_name)  # saving the final output as a PNG file
        else:
            image_name = "E:/Final Project/Implementation/FinalProject/dataset/datasetFinal/butera/sisay" + str(
                index) + ".jpg"
            data.save(image_name)  # saving the final output as a PNG file

    def _save_images_csv(self, face, index):
        sample_images = []
        sample_images = face
        sample_images = sample_images.reshape(1, -1)  # To make it 2D
        image_name = "C:/Users/Hello/FR/photos/nomalizedImages/" + str(index) + "dataedited.csv"
        savetxt(image_name, sample_images, delimiter=',')

    def __detect_face(self):
        return self.detector.detect_faces(self.image)

    def __extract_face(self, face):
        x1, y1, width, height = face['box']
        x2, y2 = x1 + width, y1 + height
        return self.image[y1:y2, x1:x2]

    def __resize_img_to_face(self, face):
        image = Image.fromarray(face)
        image = image.resize((243, 320))
        return asarray(image)

    def __plot_face(self, face):
        pyplot.imshow(face)
        pyplot.show()
