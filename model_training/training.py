from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.callbacks import Callback

IMAGE_SIZE = 32  # px
BATCH_SIZE = 16

model = Sequential()
model.add(Conv2D(64, (5, 5), input_shape=(IMAGE_SIZE, IMAGE_SIZE, 1)))
model.add(Activation('softplus'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(128, (3, 3)))
model.add(Activation('softplus'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(256, (2, 2)))
model.add(Activation('softplus'))

model.add(Flatten())
model.add(Dense(128, activation="softplus"))
model.add(Dropout(0.3))
model.add(Dense(32, activation="softplus"))
model.add(Dropout(0.3))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.summary()

datagenerator = ImageDataGenerator(rotation_range=30,
                                   width_shift_range=0.1,
                                   height_shift_range=0.1,
                                   brightness_range=(0.9, 1.1),
                                   shear_range=0.1,
                                   zoom_range=0.1,
                                   rescale=1/255,
                                   fill_mode='nearest',
                                   validation_split=0)

train_data = datagenerator.flow_from_directory("mrlEyes_open_closed/train",
                                               classes=["open", "closed"],
                                               target_size=(IMAGE_SIZE, IMAGE_SIZE),
                                               batch_size=BATCH_SIZE,
                                               color_mode="grayscale",
                                               subset="training",
                                               class_mode="binary",
                                               shuffle=True)

validation_data = datagenerator.flow_from_directory("mrlEyes_open_closed/valid",
                                                    classes=["open", "closed"],
                                                    target_size=(IMAGE_SIZE, IMAGE_SIZE),
                                                    batch_size=BATCH_SIZE,
                                                    color_mode="grayscale",
                                                    subset="training",
                                                    class_mode="binary")

model.fit(train_data,
          steps_per_epoch=train_data.samples // BATCH_SIZE,
          epochs=15,
          validation_data=validation_data,
          validation_steps=validation_data.samples // BATCH_SIZE,
          callbacks=[])
model.save('trained_models/eye_blink_3_32x.h5')
