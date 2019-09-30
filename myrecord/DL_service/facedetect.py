import cv2
import numpy as np
from mtcnn.mtcnn import MTCNN
import os


def load_image(filename):
    if not os.path.isfile(filename):
        return None
    cap = cv2.imread(filename)
    return cap


def face_detection(filename, output_filename):
    image = load_image(filename)
    if image is None:
        return None

    net = MTCNN()
    faces = net.detect_faces(image)

    for face in faces:
        x, y, w, h = face['box']
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

    pos = filename.rindex('.')
    #outputFile = filename[:pos] + "faces" + filename[pos:]
    cv2.imwrite(output_filename, image)
    return True



#face_detection("419570.jpg")
