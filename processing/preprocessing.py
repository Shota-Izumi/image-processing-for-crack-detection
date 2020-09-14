# -*- coding: utf-8 -*-

import numpy as np
import glob
import os
import pathlib
from PIL import Image
from natsort import natsorted
from math import ceil

Image.MAX_IMAGE_PIXELS = 1000000000


class PreProcessing(object):
    def __init__(self,
                 original_image_dir,
                 label_image_dir,
                 dataset_outdir,
                 crop_height,
                 crop_width,
                 overlap):

        assert isinstance(crop_height / overlap, int)
        assert isinstance(crop_width / overlap, int)
        self.original_image_dir = original_image_dir
        self.label_image_dir = label_image_dir
        self.dataset_outdir = dataset_outdir
        self.crop_height = crop_height
        self.crop_width = crop_width
        self.overlap = overlap

    def make_pathlist(self, path):
        """指定されたpathから[jpg, png]のパスリストを作成

        Args:
            path (str): 画像郡へのディレクトリ，または画像へのパス．拡張子png推奨

        Returns:
            list: 画像郡のパスリスト
        """
        image_path = pathlib.Path(path)
        if image_path.is_dir():
            image_path_list_png = glob.glob(path + '/*.png')
            image_path_list_jpg = glob.glob(path + '/*.jpg')
            image_path_list = natsorted(image_path_list_png + image_path_list_jpg)
        else:
            image_path_list = [path]
        return image_path_list

    def shuffle_index(self, noimages, train_ratio, val_ratio, test_ratio):
        assert noimages > 1
        assert train_ratio + val_ratio + test_ratio == 1.0
        imindex = list(range(noimages))
        np.random.shuffle(imindex)
        train_index = int(noimages * train_ratio)
        val_index = int(train_index + noimages * val_ratio)
        train_data = imindex[0: train_index]
        val_data = imindex[train_index: val_index]
        test_data = imindex[val_index: noimages]
        return train_data, val_data, test_data

    def make_folders(self):
        self.datasetdir = os.path.join(self.dataset_outdir, "dataset")
        self.originaldir = os.path.join(self.datasetdir, "dataset")
        self.labeldir = os.path.join(self.datasetdir, "label")
        os.makedirs(self.datasetdir, exist_ok=True)
        for f in ['train', 'val', 'test']:
            os.makedirs(os.path.join(self.originaldir, f), exist_ok=True)
            os.makedirs(os.path.join(self.labeldir, f), exist_ok=True)

    def add_margin(self, pil_img, top, right, bottom, left, color):
        width, height = pil_img.size
        new_width = width + right + left
        new_height = height + top + bottom
        result = Image.new(pil_img.mode, (new_width, new_height), color)
        result.paste(pil_img, (left, top))
        return result

    def padding(self, pil_image):
        w, h = pil_image.size
        vertical = int((ceil(h / (self.crop_height / self.overlap)) * (self.crop_height / self.overlap) - h) / 2)
        holizontal = int((ceil(w / (self.crop_width / self.overlap)) * (self.crop_width / self.overlap) - w) / 2)
        if pil_image.mode == 'RGB':
            padding_image = self.add_margin(pil_image, vertical, holizontal, vertical, holizontal, (0, 0, 0))
        else:
            padding_image = self.add_margin(pil_image, vertical, holizontal, vertical, holizontal, (0))
        return padding_image
