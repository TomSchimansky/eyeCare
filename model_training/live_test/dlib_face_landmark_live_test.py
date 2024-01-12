import cv2
import dlib

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("../dlib_models/shape_predictor_68_face_landmarks.dat")

camera = cv2.VideoCapture(0)

while True:
    ret, image = camera.read()
    image_gray = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)

    faces = detector(image_gray)
    for face in faces:

        landmarks = predictor(image=image_gray, box=face)

        for n in range(0, 68):
            x, y = landmarks.part(n).x, landmarks.part(n).y
            cv2.circle(img=image, center=(x, y), radius=3, color=(0, 255, 0), thickness=-1)

    cv2.imshow('dlib Face-Detector', image)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


