import cv2
import numpy as np
import os


def load_net():
    return cv2.dnn.readNetFromDarknet("myrecord/DL_service/classify_weights/darknet19_448.cfg",
                                      "myrecord/DL_service/classify_weights/darknet19_448.weights")


def load_classname():
    lines = open("myrecord/DL_service/classify_weights/synset_words.txt", "r").read().strip().split("\n")
    class_name = [line[line.index(" ") + 1:].split(',')[0] for line in lines]
    return class_name


def load_image(filename):
    if not os.path.isfile(filename):
        return None
    cap = cv2.imread(filename)
    return cap


def classify_image(filename):
    frame = load_image(filename)
    if frame is None:
        return None

    print("111")
    net = load_net()
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    blob = cv2.dnn.blobFromImage(frame, 1 / 255, (448, 448), [0, 0, 0], False, crop=False)
    net.setInput(blob)
    print("222")
    pred = net.forward()
    class_name = load_classname()
    print("333")
    pred = pred[0][:, 0][:, 0]
    print(pred)
    idxs = np.argsort(pred)[::-1][:3]
    print()
    ans = []
    print(idxs)
    for idx in idxs:
        print(idx)
        idx = idx
        ans.append(class_name[idx])
        print(class_name[idx])
        print(pred[idx])
    return class_name[idxs[0]]


#classify_image("images/traffic_light.png")

