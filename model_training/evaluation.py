from keras.preprocessing.image import ImageDataGenerator
import keras

IMAGE_SIZE = 32
BATCH_SIZE = 16

test_datagenerator = ImageDataGenerator(rescale=1 / 255)
test_data = test_datagenerator.flow_from_directory("mrlEyes_open_closed/test",
                                                   classes=["open", "closed"],
                                                   target_size=(IMAGE_SIZE, IMAGE_SIZE),
                                                   batch_size=BATCH_SIZE,
                                                   color_mode="grayscale",
                                                   class_mode="binary")

model = keras.models.load_model("trained_models/model_32_012-0.989.hdf5")
model.compile(metrics=["accuracy",
                       keras.metrics.Precision(),
                       keras.metrics.Recall(),
                       keras.metrics.FalsePositives(),
                       keras.metrics.FalseNegatives()])
results = model.evaluate(test_data, batch_size=BATCH_SIZE)
results_dict = dict(zip(model.metrics_names, results))
print(results_dict)
print("false positive rate:", results_dict["false_positives"] / test_data.samples)
print("false negative rate:", results_dict["false_negatives"] / test_data.samples)
