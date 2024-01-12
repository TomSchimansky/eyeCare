from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.callbacks import Callback
import os

from model_evaluation.real_accuracy_test import test_accuracy

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_SIZE = 32  # px
BATCH_SIZE = 16

model = Sequential()
model.add(Conv2D(64, (4, 4), input_shape=(IMAGE_SIZE, IMAGE_SIZE, 1)))
model.add(Activation('softplus'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(128, (3, 3)))
model.add(Activation('softplus'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(256, (2, 2)))
model.add(Activation('softplus'))

model.add(Flatten())
model.add(Dense(128))
model.add(Activation('softplus'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

model.summary()


datagenerator = ImageDataGenerator(rotation_range=30,
                                   width_shift_range=0.1,
                                   height_shift_range=0.1,
                                   rescale=1./255,
                                   shear_range=0.1,
                                   zoom_range=0.1,
                                   horizontal_flip=True,
                                   fill_mode='nearest',
                                   validation_split=0.0)

train_data = datagenerator.flow_from_directory(
    ROOT_DIR + "/data/mrlEyes_2018_01/train",
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE,
    color_mode="grayscale",
    subset="training",
    class_mode='binary')

validation_data = datagenerator.flow_from_directory(
    ROOT_DIR + "/data/mrlEyes_2018_01/validation",
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE,
    color_mode="grayscale",
    subset="training",
    class_mode='binary')


class AccuracyCallback(Callback):
    def on_epoch_end(self, epoch, logs=None):
        real_acc = test_accuracy(self.model, 1000)

        if real_acc > 0.98:
            self.model.stop_training = True


model.fit_generator(train_data,
                    steps_per_epoch=train_data.samples // BATCH_SIZE,
                    epochs=15,
                    validation_data=validation_data,
                    validation_steps=validation_data.samples // BATCH_SIZE,
                    callbacks=[AccuracyCallback()])
model.save('trained_models/eye_blink_3_32x.h5')


