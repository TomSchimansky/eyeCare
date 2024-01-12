import cv2
import numpy as np
import threading
import time
from settings import Settings
from app_analyzing.cv2_camera import Cv2Camera
from app_analyzing.timing import StopWatch


class EyeAnalyzer(threading.Thread):

    # camera
    X_RESOLUTION = 640
    Y_RESOLUTION = 480

    # detection
    IMAGE_SIZE = 32  # eye crop pixel size
    EYE_BOX_SIZE_FACTOR = 1.2  # margin around eye when cropping
    NUMBER_OF_BLACKOUTS_TILL_RESET = 3  # time_of_last_blink will switch to None after it
    THRESHOLD_FOR_BLINK_DETECTION = 0.4  # between 0-1
    LONGEST_POSSIBLE_BLINK_TIME = 0.5  # shorter blinks don't raise the counter

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setDaemon(True)

        self.face_detector = None
        self.face_68_shape_detector = None
        self.eye_blink_keras_model = None
        self.camera = None

        self.running = False
        self.paused = True
        self.start_loading_now = False

        self.loading_status = 0
        self.time_of_last_blink = None
        self.blackout_counter = 0
        self.blink_counter = 0
        self.up_time_stopwatch = StopWatch()

    def load(self):
        self.camera = Cv2Camera(self.X_RESOLUTION, self.Y_RESOLUTION)
        self.loading_status = 0.1

        import dlib
        self.loading_status = 0.2

        import keras
        self.loading_status = 0.6

        self.face_detector = dlib.get_frontal_face_detector()
        self.loading_status = 0.8

        self.face_68_shape_detector = dlib.shape_predictor(Settings.MAIN_PATH
                                                           + "/ml_models/dlib/shape_predictor_68_face_landmarks.dat")
        self.loading_status = 0.9

        self.eye_blink_keras_model = keras.models.load_model(Settings.MAIN_PATH
                                                             + '/ml_models/tensorflow/eye_blink_3_32x.h5')
        self.loading_status = 1.0

    @staticmethod
    def get_eye_box_from_landmarks(landmarks, n1, n2):
        box_size_factor = 1.2
        eye_width = round((landmarks.part(n2).x - landmarks.part(n1).x) * box_size_factor)

        eye1_x = round((landmarks.part(n1).x + landmarks.part(n2).x) / 2)
        eye1_y = round((landmarks.part(n1).y + landmarks.part(n2).y) / 2)

        return eye1_x, eye1_y, eye_width

    @property
    def time_since_last_blink(self):
        if self.time_of_last_blink is not None:
            return time.time()-self.time_of_last_blink
        else:
            return None

    def start_loading(self):
        self.start_loading_now = True

    def activate_analyzing(self):
        self.paused = False

    def deactivate_analyzing(self):
        self.paused = True

    def stop(self):
        self.running = False

    def get_average_blink_time(self):
        if self.blink_counter > 0:
            return self.up_time_stopwatch.get_elapsed() / self.blink_counter
        else:
            return 0

    def reset_blink_counter(self):
        self.blink_counter = 0
        self.up_time_stopwatch.reset()

    def run(self):
        while not self.running:
            if self.start_loading_now:
                self.load()
                self.running = True
            else:
                time.sleep(0.1)

        while self.running:
            if not self.paused:

                if self.camera.is_open is not True:
                    self.camera.open()

                # get camera grayscale image
                gray_image = self.camera.get_gray_image()
                if gray_image is not None:

                    # detect faces in image
                    faces = self.face_detector(gray_image)
                    if faces:

                        self.up_time_stopwatch.start()

                        # sort faces by size (width)
                        faces = sorted(faces, key=lambda x: abs(x.left()-x.right()), reverse=True)

                        # predict landmarks of largest face in image
                        landmarks = self.face_68_shape_detector(image=gray_image, box=faces[0])

                        # crop image of left eye
                        eye1_x, eye1_y, eye1_width = self.get_eye_box_from_landmarks(landmarks, 36, 39)
                        eye_region_1 = gray_image[eye1_y - eye1_width:eye1_y + eye1_width,
                                                  eye1_x - eye1_width:eye1_x + eye1_width]

                        # crop image of right eye
                        eye2_x, eye2_y, eye2_width = self.get_eye_box_from_landmarks(landmarks, 42, 45)
                        eye_region_2 = gray_image[eye2_y - eye2_width:eye2_y + eye2_width,
                                                  eye2_x - eye2_width:eye2_x + eye2_width]

                        # resize eye images to IMAGE_SIZE x IMAGE_SIZE size
                        eye_region_1 = cv2.resize(eye_region_1, (self.IMAGE_SIZE, self.IMAGE_SIZE)) / 255
                        eye_region_2 = cv2.resize(eye_region_2, (self.IMAGE_SIZE, self.IMAGE_SIZE)) / 255

                        # create input batch for keras model
                        image_batch = np.zeros(self.IMAGE_SIZE * self.IMAGE_SIZE * 2).reshape(2, self.IMAGE_SIZE, self.IMAGE_SIZE, 1)
                        image_batch[0] = eye_region_1.reshape(self.IMAGE_SIZE, self.IMAGE_SIZE, 1)
                        image_batch[1] = eye_region_2.reshape(self.IMAGE_SIZE, self.IMAGE_SIZE, 1)

                        # run keras eye blink detection model on batch
                        out = self.eye_blink_keras_model.predict(image_batch, batch_size=2)
                        if out[0][0] < self.THRESHOLD_FOR_BLINK_DETECTION and out[1][0] < self.THRESHOLD_FOR_BLINK_DETECTION:
                            # eye blink detected

                            if self.time_of_last_blink is not None:
                                if time.time()-self.time_of_last_blink > self.LONGEST_POSSIBLE_BLINK_TIME:
                                    self.blink_counter += 1
                            else:
                                self.blink_counter += 1

                            self.time_of_last_blink = time.time()
                            self.blackout_counter = 0

                    else:
                        # no face detected
                        self.up_time_stopwatch.stop()
                        self.blackout_counter += 1
                        if self.blackout_counter >= self.NUMBER_OF_BLACKOUTS_TILL_RESET:
                            self.time_of_last_blink = None

                else:
                    # no camera image
                    self.up_time_stopwatch.stop()
                    self.blackout_counter += 1
                    if self.blackout_counter >= self.NUMBER_OF_BLACKOUTS_TILL_RESET:
                        self.time_of_last_blink = None

            else:
                # analyzing is paused
                self.up_time_stopwatch.stop()
                if self.camera.is_open:
                    self.camera.close()

                self.time_of_last_blink = None
                time.sleep(0.1)


if __name__ == "__main__":
    # simple test program

    e = EyeAnalyzer()
    e.start()
    e.start_loading()
    e.activate_analyzing()

    while True:
        print(f"Time since last blink: {e.time_since_last_blink}")