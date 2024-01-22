# Imports
import os
import pandas as pd
import torch
from torch.utils.data import Dataset
from skimage import io

# Dataset class, from: https://www.youtube.com/watch?v=ZoZHd0Zm3RY
# Reads a csv file with image paths and labels
# dataset[i] returns tuple with ith image and label
class ImageDataset(Dataset):
    def __init__(self, csv_file, root_dir, transform=None):
        self.annotations = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, index):
        img_path = os.path.join(self.root_dir, self.annotations.iloc[index, 0])
        image = io.imread(img_path)
        y_label = int(self.annotations.iloc[index, 1])

        if self.transform:
            image = self.transform(image)
        print(image.shape)
        return (image, y_label)