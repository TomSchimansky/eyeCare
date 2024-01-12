import cv2


class Cv2Camera:
    """ simple wrapper around the cv2.VideoCapture:

     c = Cv2Camera(640, 480)
     c.open()
     image_1 = c.get_rgb_image()
     image_2 = c.get_gray_image()
     c.close()

     c.change_video_device(1)
     c.set_resolution(1280, 720)
     c.open()
     image_3 = c.get_rgb_image()
     c.close()

    """

    def __init__(self, x_res, y_res, video_device=0):
        self.camera = None
        self.x_res = x_res
        self.y_res = y_res
        self.video_device = video_device

    def open(self):
        if self.camera is None:
            self.camera = cv2.VideoCapture(self.video_device)
            self.set_resolution(self.x_res, self.y_res)

            if not self.camera.isOpened():
                self.camera.open()

    def close(self):
        if self.camera is not None:
            self.camera.release()
            self.camera = None

    @property
    def is_open(self):
        if self.camera is not None:
            return True
        else:
            return False

    def change_video_device(self, video_device):
        """ camera needs to be closed to change the video device """

        self.video_device = video_device

    def set_resolution(self, x_res, y_res):
        if self.camera is not None:
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, int(x_res))
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y_res))

    def get_gray_image(self):
        """ camera needs to be open """

        if self.camera is not None:
            status, image = self.camera.read()
            if status is True:
                return cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)
            else:
                return None
        else:
            return None

    def get_rgb_image(self):
        """ camera needs to be open """

        if self.camera is not None:
            status, image = self.camera.read()
            if status is True:
                return cv2.cvtColor(src=image, code=cv2.COLOR_BGR2RGB)
            else:
                return None
        else:
            return None
