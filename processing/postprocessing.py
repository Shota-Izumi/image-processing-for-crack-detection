
# -*- coding: utf-8 -*-

import numpy as np
import glob
import os
import pathlib
from PIL import Image
from natsort import natsorted
from math import ceil

Image.MAX_IMAGE_PIXELS = 1000000000


class PostProcessing(object):
    def __init__(self,
                 original_image_dir,
                 predicted_image_dir,
                 label_image_dir,
                 outdir,
                 crop_height,
                 crop_width,
                 overlap):

        assert isinstance(crop_height / overlap, int)
        assert isinstance(crop_width / overlap, int)
        self.original_image_dir = original_image_dir
        self.predicted_image_dir = predicted_image_dir
        self.label_image_dir = label_image_dir
        self.outdir = outdir
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

    def make_imagesizelist(self, label_path):
        pathlist = self.make_pathlist(label_path)
        image_nameandsize_dict = {}
        for p in pathlist:
            name = os.path.basename(p).split('.')[0]
            w, h = Image.open(p).size
            vertical_margin = int((ceil(h / (self.crop_height / self.overlap)) \
                                   * (self.crop_height / self.overlap) - h) / 2)
            holizontal_margin = int((ceil(w / (self.crop_width / self.overlap)) \
                                     * (self.crop_width / self.overlap) - w) / 2)
            image_nameandsize_dict[name] = [
                (w, h),
                (w + holizontal_margin * 2, h + vertical_margin * 2)
                ]
        return image_nameandsize_dict
