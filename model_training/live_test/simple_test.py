import keras
import numpy as np
from PIL import Image

from config import *

open_image = os.listdir(ROOT_DIR + "/data/mrlEyes_2018_01/validation/open")
closed_image = os.listdir(ROOT_DIR + "/data/mrlEyes_2018_01/validation/closed")


def load_image(state, n):
    if state == "open":
        image = Image.open(ROOT_DIR + "/data/mrlEyes_2018_01/validation/" + state + "/" + open_image[n])
    if state == "closed":
        image = Image.open(ROOT_DIR + "/data/mrlEyes_2018_01/validation/" + state + "/" + closed_image[n])
    image = image.resize((IMAGE_SIZE, IMAGE_SIZE))
    image = image.convert("L")
    image.show()
    image = np.array(image.getdata())/255
    return image


model = keras.models.load_model(ROOT_DIR + '/trained_models/eye_blink_3_32x.h5')

for i in range(10):
    image = load_image("closed", i)
    image_batch = image.reshape(1, IMAGE_SIZE, IMAGE_SIZE, 1)
    out = model.predict(image_batch, batch_size=1)
    print("Model output:", out)