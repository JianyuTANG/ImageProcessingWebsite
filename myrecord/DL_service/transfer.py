import cv2
import os


def load_image(filename):
    if not os.path.isfile(filename):
        return None
    cap = cv2.imread(filename)
    return cap


def load_net(i):
    net = None
    if i == 1:
        net = cv2.dnn.readNetFromTorch("myrecord/DL_service/transfer_models/the_scream.t7")
    elif i == 2:
        net = cv2.dnn.readNetFromTorch("myrecord/DL_service/transfer_models/candy.t7")
    elif i == 3:
        net = cv2.dnn.readNetFromTorch("myrecord/DL_service/transfer_models/composition.t7")
    elif i == 4:
        net = cv2.dnn.readNetFromTorch("myrecord/DL_service/transfer_models/feathers.t7")
    elif i == 5:
        net = cv2.dnn.readNetFromTorch("myrecord/DL_service/transfer_models/la_muse.t7")
    elif i == 6:
        net = cv2.dnn.readNetFromTorch("myrecord/DL_service/transfer_models/mosaic.t7")
    elif i == 7:
        net = cv2.dnn.readNetFromTorch("myrecord/DL_service/transfer_models/starry_night.t7")
    elif i == 8:
        net = cv2.dnn.readNetFromTorch("myrecord/DL_service/transfer_models/the_wave.t7")
    else:
        net = cv2.dnn.readNetFromTorch("myrecord/DL_service/transfer_models/udnie.t7")
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    return net


def transfer_image(filename, output_filename, i):
    img = load_image(filename)
    if img is None:
        return None

    net = load_net(i)

    h, w = img.shape[:2]
    blob = cv2.dnn.blobFromImage(img, 1.0, (w, h), (103.9, 116.8, 123.7),
                                 swapRB=False, crop=False)

    net.setInput(blob)
    out = net.forward()

    out = out.reshape(3, out.shape[2], out.shape[3])
    out[0] += 103.9
    out[1] += 116.8
    out[2] += 123.7
    out = out.transpose(1, 2, 0)

    pos = filename.rindex('.')
    #outputFile = filename[:pos] + "_transfered" + str(i) + filename[pos:]
    cv2.imwrite(output_filename, out)
    return True



#transfer_image("images/dog.jpg", 2)
