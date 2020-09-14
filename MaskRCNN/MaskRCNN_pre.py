# -*- coding: utf-8 -*-

import numpy as np
import glob
import os
import pathlib
from PIL import Image
from natsort import natsorted
from math import ceil
from ..processing.preprocessing import PreProcessing

Image.MAX_IMAGE_PIXELS = 1000000000


class MaskRCNNPreProcessing(PreProcessing):
    def __init__(self,
                 original_image_dir,
                 label_image_dir,
                 dataset_outdir,
                 crop_height,
                 crop_width,
                 overlap,
                 area_option):

        super().__init__(original_image_dir,
                         label_image_dir,
                         dataset_outdir,
                         crop_height,
                         crop_width,
                         overlap)

    def crop_and_save(self, original_image_path, label_image_path):
        basename = os.path.basename(original_image_path)
        original = Image.open(original_image_path)
        label = Image.open(label_image_path)
        width, height = original.size
        w = int((width / (self.crop_width / self.overlap)) - 1)
        h = int((height / (self.crop_height / self.overlap)) - 1)
        for x in range(w):
            for y in range(h):
                left  = (crop_width / over_lap) * x
                upper = (crop_height / over_lap) * y
                right = left + crop_width
                lower = upper + crop_height
                ori_crop = original.crop((left, upper, right, lower))
                lab_crop = label.crop((left, upper, right, lower))
                ori_crop.save(os.path.join(self.originaldir, basename + "_{0}_{1}".format(x, y)))
                lab_crop.save(os.path.join(self.labeldir, basename + "_{0}_{1}".format(x, y)))

    def optional_crop_and_save(self, original_image_path, label_image_path, save_dir, threshold):
        basename = os.path.basename(original_image_path)
        original = Image.open(original_image_path)
        label = Image.open(label_image_path)
        width, height = original.size
        w = int((width / (self.crop_width / self.overlap)) - 1)
        h = int((height / (self.crop_height / self.overlap)) - 1)
        for x in range(w):
            for y in range(h):
                left  = (crop_width / over_lap) * x
                upper = (crop_height / over_lap) * y
                right = left + crop_width
                lower = upper + crop_height
                ori_crop = original.crop((left, upper, right, lower))
                lab_crop = label.crop((left, upper, right, lower))
                lab_crop_array = np.array(lab_crop).astype(np.uint8)
                if lab_crop_array[np.nonzero(lab_crop_array)].shape[0] > threshold:
                    ori_crop.save(os.path.join(self.originaldir, basename + "_{0}_{1}".format(x, y)))
                    lab_crop.save(os.path.join(self.labeldir, basename + "_{0}_{1}".format(x, y)))
