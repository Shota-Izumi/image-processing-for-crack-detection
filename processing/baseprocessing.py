# -*- coding: utf-8 -*-

import numpy as np
import glob
import os
import pathlib
from PIL import Image
from natsort import natsorted


class BaseProcessing(object):
    def __init__(self,
                 original_image_dir,
                 crop_height,
                 crop_width,
                 overlap):

        self.original_image_dir = original_image_dir
        self.crop_height = crop_height
        self.crop_width = crop_width
        self.overlap = overlap

    def
