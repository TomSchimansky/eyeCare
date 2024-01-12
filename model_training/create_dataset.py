"""
Copy images of mrlEyes_2018_01 into mrlEyes_open_closed and split into the following directories:
train/open, train/closed
valid/open, valid/closed
test/open, test/closed

Number of valid and test files are chosen according to parameters:
valid_split
test_split

Original mrlEyes_2018_01 dataset download: http://mrl.cs.vsb.cz/data/eyedataset/mrlEyes_2018_01.zip
"""

import os
import math
from PIL import Image

valid_split = 0.02
test_split = 0.08
mrlEyes_2018_01_path = "./mrlEyes_2018_01"  # original dataset
mrlEyes_open_closed_path = "./mrlEyes_open_closed"  # new dataset
mrlEyes_open_closed_resolution = 64  # px


def create_folder_if_not_exists(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

# create folders
create_folder_if_not_exists(mrlEyes_open_closed_path)
create_folder_if_not_exists(mrlEyes_open_closed_path + "/train")
create_folder_if_not_exists(mrlEyes_open_closed_path + "/valid")
create_folder_if_not_exists(mrlEyes_open_closed_path + "/test")
create_folder_if_not_exists(mrlEyes_open_closed_path + "/train/open")
create_folder_if_not_exists(mrlEyes_open_closed_path + "/train/closed")
create_folder_if_not_exists(mrlEyes_open_closed_path + "/valid/open")
create_folder_if_not_exists(mrlEyes_open_closed_path + "/valid/closed")
create_folder_if_not_exists(mrlEyes_open_closed_path + "/test/open")
create_folder_if_not_exists(mrlEyes_open_closed_path + "/test/closed")

# create list of all image files in original dataset
file_names_list = []
for directory in os.scandir(mrlEyes_2018_01_path):
    if directory.is_dir():
        sub_entries = os.scandir(directory.path)
        for file in sub_entries:
            if file.is_file() and file.name.endswith(".png"):
                file_names_list.append(file.path)

# separate open and closed eye images
file_names_list_open = []
file_names_list_closed = []
for file_name_path in file_names_list:
    file_name = file_name_path.split("/")[-1]
    raw_file_name = file_name.split(".")[0]
    raw_file_name_parts = raw_file_name.split("_")

    if raw_file_name_parts[4] == "0":
        file_names_list_closed.append(file_name_path)
    elif raw_file_name_parts[4] == "1":
        file_names_list_open.append(file_name_path)

print(f"mrlEyes_2018_01 images: {len(file_names_list)}")
print(f"mrlEyes_2018_01 images open: {len(file_names_list_open)}")
print(f"mrlEyes_2018_01 images closed: {len(file_names_list_closed)}")

# calculate number of images
number_of_image_per_class = min(len(file_names_list_open), len(file_names_list_closed))
number_of_image_per_class_test = math.floor(number_of_image_per_class * test_split)
number_of_image_per_class_valid = math.floor(number_of_image_per_class * valid_split)
number_of_image_per_class_train = number_of_image_per_class - number_of_image_per_class_test - number_of_image_per_class_valid

print(f"mrlEyes_open_closed train: {number_of_image_per_class_train * 2}")
print(f"mrlEyes_open_closed valid: {number_of_image_per_class_valid * 2}")
print(f"mrlEyes_open_closed test: {number_of_image_per_class_test * 2}")


def resize_and_copy_image(image_path, destination_folder, resolution):
    image = Image.open(image_path)
    image = image.resize((resolution, resolution))
    image.save(os.path.join(destination_folder, os.path.basename(image_path)))


# load, resize and save images to new folders
for i, (image_path_open, image_path_closed) in enumerate(zip(file_names_list_open, file_names_list_closed)):
    if i < number_of_image_per_class_train:  # train
        resize_and_copy_image(image_path_open, mrlEyes_open_closed_path + "/train/open", mrlEyes_open_closed_resolution)
        resize_and_copy_image(image_path_closed, mrlEyes_open_closed_path + "/train/closed", mrlEyes_open_closed_resolution)

    elif i < number_of_image_per_class_train + number_of_image_per_class_valid:  # valid
        resize_and_copy_image(image_path_open, mrlEyes_open_closed_path + "/valid/open", mrlEyes_open_closed_resolution)
        resize_and_copy_image(image_path_closed, mrlEyes_open_closed_path + "/valid/closed", mrlEyes_open_closed_resolution)

    else:  # test
        resize_and_copy_image(image_path_open, mrlEyes_open_closed_path + "/test/open", mrlEyes_open_closed_resolution)
        resize_and_copy_image(image_path_closed, mrlEyes_open_closed_path + "/test/closed", mrlEyes_open_closed_resolution)

