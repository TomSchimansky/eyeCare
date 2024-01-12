import keras
import numpy as np
from PIL import Image

from config import *

open_image = os.listdir(ROOT_DIR + "/data/mrlEyes_2018_01/validation/open")
closed_image = os.listdir(ROOT_DIR + "/data/mrlEyes_2018_01/validation/closed")


def load_image(state, n, show=False):
    if state == "open":
        image = Image.open(ROOT_DIR + "/data/mrlEyes_2018_01/validation/" + state + "/" + open_image[n])
    elif state == "closed":
        image = Image.open(ROOT_DIR + "/data/mrlEyes_2018_01/validation/" + state + "/" + closed_image[n])

    image = image.resize((IMAGE_SIZE, IMAGE_SIZE))
    image = image.convert("L")

    if show:
        image.show()
    image = np.array(image.getdata())/255

    return image


def test_accuracy(model, n):
    open_hit_counter = 0
    close_hit_counter = 0

    test_batch = np.zeros(n * IMAGE_SIZE * IMAGE_SIZE * 1).reshape(n, IMAGE_SIZE, IMAGE_SIZE, 1)

    for i in range(n):
        image = load_image("open", i).reshape(IMAGE_SIZE, IMAGE_SIZE, 1)
        test_batch[i] = image
    result = model.predict(test_batch, batch_size=n)

    for entry in result:
        if entry[0] > 0.5:
            open_hit_counter += 1

    test_batch = np.zeros(n * IMAGE_SIZE * IMAGE_SIZE * 1).reshape(n, IMAGE_SIZE, IMAGE_SIZE, 1)

    for i in range(n):
        image = load_image("closed", i).reshape(IMAGE_SIZE, IMAGE_SIZE, 1)
        test_batch[i] = image
    result = model.predict(test_batch, batch_size=n)

    for entry in result:
        if entry[0] <= 0.5:
            close_hit_counter += 1

    print("[Accuracy Test] n:", n,
          " - Right Answers open:", open_hit_counter, "/", n,
          " - Right Answers close:", close_hit_counter, "/", n,
          " - Overall-Accuracy:", (open_hit_counter+close_hit_counter)/(2*n))

    return (open_hit_counter+close_hit_counter)/(2*n)


if __name__ == "__main__":
    model = keras.models.load_model(ROOT_DIR + '/trained_models/eye_blink_3_32x.h5')
    test_accuracy(model, 3000)
