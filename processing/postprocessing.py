# -*- coding: utf-8 -*-

import numpy as np
import glob
import os
import pathlib
from PIL import Image
from natsort import natsorted
from math import ceil

Image.MAX_IMAGE_PIXELS = 1000000000