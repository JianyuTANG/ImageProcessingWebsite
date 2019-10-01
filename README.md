# Image Processing Website
A Django website (incld front and back end) using Deep Learning to process images.

## To Run the service

you need...

#### environment

- python 3.6/7

- \>=Django 2.1
- \>=OpenCV 4.1
- MTCNN
- \>=TensorFlow 1.4

#### models for deep neural networks

- download **darknet19_448.weights** from [here](  https://github.com/pjreddie/darknet) and put it in 

  ```
  ImageProcessingWebsite\myrecord\DL_service\classify_weights
  ```

- download **yolov3.weights** from [here](  https://github.com/pjreddie/darknet) and put it in

  ```
  ImageProcessingWebsite\myrecord\DL_service\detect_weights
  ```

- download weights for transfer models from [here](https://github.com/jcjohnson/fast-neural-style) and put it in

  ```
  ImageProcessingWebsite\myrecord\DL_service\transfer_models
  ```




### Acknowledgement

Collaborated with Yingqi Wang(汪颖祺) and thanks for her hard work in our project.

