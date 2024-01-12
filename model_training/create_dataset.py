import shutil

from config import *


class DataLoader(object):
    """ MRL Eye Dataset:
    In the dataset, we collected the data of 37 different persons (33 men and 4 women)

    explanation of file names: data/mrlEyes_2018_01/annotations.txt """

    def __init__(self):
        self.file_names_list = []
        self.main_path = ROOT_DIR
        self.path_to_orig_data = ""
        self.new_dataset_folder = self.main_path + "/data/mrlEyes_2018_01"

        print(self.main_path)
        print(self.new_dataset_folder)

    def separate_open_closed(self):
        """ needs to be called only once to split images from MRL-Dataset
        into open and closed eyes folders """

        entries = os.scandir(self.path_to_orig_data)
        for directory in entries:
            if directory.is_dir():
                sub_entries = os.scandir(directory.path)
                for file in sub_entries:
                    if file.is_file() and file.name.endswith(".png"):
                        self.file_names_list.append(file.path)

        try:
            os.mkdir(self.new_dataset_folder + "/train/closed")
            os.mkdir(self.new_dataset_folder + "/train/open")
        except FileExistsError:
            pass

        for file_name_path in self.file_names_list:
            file_name = file_name_path.split("/")[-1]
            raw_file_name = file_name.split(".")[0]
            raw_file_name_parts = raw_file_name.split("_")

            if raw_file_name_parts[4] == "0":
                shutil.copy(file_name_path, self.new_dataset_folder + "/train/closed")
            elif raw_file_name_parts[4] == "1":
                shutil.copy(file_name_path, self.new_dataset_folder + "/train/open")

    def seperate_train_validation(self, number_of_validation_images):
        """ moves given number of images from train folder to validation folder """

        # images = os.listdir(self.new_dataset_folder + "/validation")
        # for image in images:
        #     if "closed" in image and "png" in image:
        #         shutil.move(self.new_dataset_folder + "/validation/" + image,
        #                     self.new_dataset_folder + "/train/closed/" + image.replace("closed", ""))
        #     if "open" in image and "png" in image:
        #         shutil.move(self.new_dataset_folder + "/validation/" + image,
        #                     self.new_dataset_folder + "/train/open/" + image.replace("open", ""))

        try:
            os.mkdir(self.new_dataset_folder + "/validation/closed")
            os.mkdir(self.new_dataset_folder + "/validation/open")
        except FileExistsError:
            pass

        closed_images = os.listdir(self.new_dataset_folder + "/train/closed")
        open_images = os.listdir(self.new_dataset_folder + "/train/open")
        for image in closed_images[-number_of_validation_images:]:
            shutil.move(self.new_dataset_folder + "/train/closed/" + image,
                        self.new_dataset_folder + "/validation/closed/" + image)

        for image in open_images[-number_of_validation_images:]:
            shutil.move(self.new_dataset_folder + "/train/open/" + image,
                        self.new_dataset_folder + "/validation/open/" + image)


if __name__ == "__main__":
    data = DataLoader()
    data.seperate_train_validation(3000)