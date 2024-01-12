# eyeCare

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

## Model training and evaluation

Download mrlEyes_2018_01 and create mrlEyes_open_closed dataset with images separated into train, vlaid and test folders with open and closed folders each:
```
wget http://mrl.cs.vsb.cz/data/eyedataset/mrlEyes_2018_01.zip
unzip mrlEyes_2018_01.zip
cd model_training
python create_dataset.py
```
(Can take a few minutes)

Train CNN classifier model and copy best model to model_training/trained_models and app/ml_models/tensorflow:
```
python training.py
cd checkpoints
cp best_model.hdf5 ../trained_models
cp best_model.hdf5 ../../app/ml_models/tensorflow
```
(Training takes approximately 15 minutes for 50 epochs on Nvidia RTX3070)

Evaluation on test dataset not used in training process:
```
python evaluation.py
```
