import cv2
import dlib
import keras
import numpy as np

from config import *

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(ROOT_DIR + "/dlib_models/shape_predictor_68_face_landmarks.dat")

model = keras.models.load_model(ROOT_DIR + '/trained_models/eye_blink_3_32x.h5')

image = cv2.imread('image.jpeg')
image = cv2.resize(image, (1024, 1024))
image_gray = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)

faces = detector(image_gray)
for face in faces:

    landmarks = predictor(image=image_gray, box=face)

    def get_eye_box_from_landmarks(landmarks, n1, n2):
        eye_width = round((landmarks.part(n2).x - landmarks.part(n1).x) * 1.2)

        eye1_x = round((landmarks.part(n1).x + landmarks.part(n2).x) / 2)
        eye1_y = round((landmarks.part(n1).y + landmarks.part(n2).y) / 2)

        return eye1_x, eye1_y, eye_width


    eye1_x, eye1_y, eye1_width = get_eye_box_from_landmarks(landmarks, 36, 39)
    eye_region_1 = image_gray[eye1_y-eye1_width:eye1_y+eye1_width,
                              eye1_x-eye1_width:eye1_x+eye1_width]

    eye2_x, eye2_y, eye2_width = get_eye_box_from_landmarks(landmarks, 42, 45)
    eye_region_2 = image_gray[eye2_y - eye2_width:eye2_y + eye2_width,
                              eye2_x - eye2_width:eye2_x + eye2_width]

    eye_region_1 = cv2.resize(eye_region_1, (IMAGE_SIZE, IMAGE_SIZE)) / 255
    eye_region_2 = cv2.resize(eye_region_2, (IMAGE_SIZE, IMAGE_SIZE)) / 255

    image_batch = np.zeros(IMAGE_SIZE * IMAGE_SIZE * 2).reshape(2, IMAGE_SIZE, IMAGE_SIZE, 1)
    image_batch[0] = eye_region_1.reshape(IMAGE_SIZE, IMAGE_SIZE, 1)
    image_batch[1] = eye_region_2.reshape(IMAGE_SIZE, IMAGE_SIZE, 1)

    out = model.predict(image_batch, batch_size=2)
    if out[0][0] < 0.4 and out[1][0] < 0.4:
        print("blink detection: eyes closed!")
    else:
        print("blink detection: eyes open!")
