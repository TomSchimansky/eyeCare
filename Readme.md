# eyeCare - Concept

<div align="center">
  <img src="documentation_images/eyeCare_screenshot_1.png" width="600"/>
</div>

This is a concept program I developed in 2018-2020 for tackling eye strain caused by prolonged screen usage.
Problems like dry and itchy eyes are partially caused by a reduce blinking rate when staring on a screen,
which this program tries to fix by giving a subtle sound signal when no blinking is detected for a
certain time. For this, the program uses the webcam, detects the face, crops out the eye regions and runs
a classifier on the eye regions detecting an open or closed eye in real time.

## Installation and usage

Create virtual environment and install libraries:
```
python -m venv .
source bin/activate
python -m pip install -r requirements.txt
```
Run app:
```
cd app
python app.py
```

## Dataset
For training the classifier, a preprocessed version of the mrlEyes_2018_01 dataset is used, which can be created using `create_dataset.py`. The script will create
a new folder called mrlEyes_open_closed with train, valid and test folders and images from the mrlEyes_2018_01 resized to 64x64:
```
mrlEyes_open_closed/
├── train/
│   ├── open/ (37753 files)
│   └── closed/ (37753 files)
├── valid/
│   ├── open/ (838 files)
│   └── closed/ (838 files)
└── test/
    ├── open/ (3355 files)
    └── closed/ (3355 files)
```
Download mrlEyes_2018_01 and create mrlEyes_open_closed dataset:
```
wget http://mrl.cs.vsb.cz/data/eyedataset/mrlEyes_2018_01.zip
unzip mrlEyes_2018_01.zip
cd model_training
python create_dataset.py
```
(Can take a few minutes)

## Model training

The following architecture is used to classify 32x32 eye images (eye open: 0, eye closed: 1):
```
       OPERATION           DATA DIMENSIONS   WEIGHTS(N)   WEIGHTS(%)

           Input   #####     32   32    1
          Conv2D    \|/  -------------------      1664     0.2%
        softplus   #####     28   28   64
    MaxPooling2D   Y max -------------------         0     0.0%
                   #####     14   14   64
          Conv2D    \|/  -------------------    131200    16.5%
        softplus   #####     11   11  128
    MaxPooling2D   Y max -------------------         0     0.0%
                   #####      5    5  128
          Conv2D    \|/  -------------------    131328    16.6%
        softplus   #####      4    4  256
         Flatten   ||||| -------------------         0     0.0%
                   #####        4096
           Dense   XXXXX -------------------    524416    66.1%
        softplus   #####         128
         Dropout    | || -------------------         0     0.0%
                   #####         128
           Dense   XXXXX -------------------      4128     0.5%
        softplus   #####          32
         Dropout    | || -------------------         0     0.0%
                   #####          32
           Dense   XXXXX -------------------        33     0.0%
         sigmoid   #####           1
```
Train CNN classifier model and copy best model to model_training/trained_models and app/ml_models/tensorflow:
```
python training.py
cd checkpoints
cp best_model.hdf5 ../trained_models
cp best_model.hdf5 ../../app/assets/trained_models
```
(Training takes approximately 15 minutes for 50 epochs on Nvidia RTX3070)

Evaluation on test dataset with images not used in training process:
```
python evaluation.py
```
With above architecture the following metrics can be achieved on the valid dataset:
```
      Accuracy: 98.3 %
     Precision: 97.9 %
        Recall: 98.7 %
False-Positive: 1.04 %
```

## Live evaluation of model:

A trained model can be live-tested with sound feedback when blinking:
```
cd model_training/live_test
python blink_detection_live_test.py
```

<img src="documentation_images/blink_detection_live_test.png" width="500"/>


The eye regions are cropped using the Dlib shape_predictor_68_face_landmarks.dat. A live demonstration of the Dlib face and landmark detector:
```
cd model_training/live_test
python dlib_face_landmark_live_test.py
```

<img src="documentation_images/dlib_face_landmark_live_test.png" width="500"/>

For extraction of the eye regions the midpoints of landmarks 36, 39 and 42, 45 are used:

<img src="documentation_images/Dlib_Face_Landmarks.png" width="500"/>
