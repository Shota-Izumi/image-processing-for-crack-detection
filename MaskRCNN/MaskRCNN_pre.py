
# -*- coding: utf-8 -*-

import numpy as np
import os
import cv2
from PIL import Image
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
        basename = os.path.basename(original_image_path).split('.')[0]
        original = Image.open(original_image_path)
        label = Image.open(label_image_path)
        width, height = original.size
        w = int((width / (self.crop_width / self.overlap)) - 1)
        h = int((height / (self.crop_height / self.overlap)) - 1)
        for x in range(w):
            for y in range(h):
                left = (self.crop_width / self.over_lap) * x
                upper = (self.crop_height / self.over_lap) * y
                right = left + self.crop_width
                lower = upper + self.crop_height
                ori_crop = original.crop((left, upper, right, lower))
                lab_crop = label.crop((left, upper, right, lower))
                ori_crop.save(os.path.join(self.originaldir, basename + "_{0}_{1}.png".format(x, y)))
                lab_crop.save(os.path.join(self.labeldir, basename + "_{0}_{1}.png".format(x, y)))

    def optional_crop_and_save(self, original_image_path, label_image_path, save_dir, threshold):
        basename = os.path.basename(original_image_path).split('.')[0]
        original = Image.open(original_image_path)
        label = Image.open(label_image_path)
        width, height = original.size
        w = int((width / (self.crop_width / self.overlap)) - 1)
        h = int((height / (self.crop_height / self.overlap)) - 1)
        for x in range(w):
            for y in range(h):
                left = (self.crop_width / self.over_lap) * x
                upper = (self.crop_height / self.over_lap) * y
                right = left + self.crop_width
                lower = upper + self.crop_height
                ori_crop = original.crop((left, upper, right, lower))
                lab_crop = label.crop((left, upper, right, lower))
                lab_crop_array = np.array(lab_crop).astype(np.uint8)
                if lab_crop_array[np.nonzero(lab_crop_array)].shape[0] > threshold:
                    ori_crop.save(os.path.join(self.originaldir, basename + "_{0}_{1}.png".format(x, y)))
                    lab_crop.save(os.path.join(self.labeldir, basename + "_{0}_{1}.png".format(x, y)))

    def make_json(self):
        f = open(os.path.join(self.originaldir, 'via_region_data.json'), 'w')
        files = self.make_pathlist(self.labeldir)
        f.write('{')
        j = 0
        for file in files:
            # エッジ検出
            im = cv2.imread('{}'.format(file).format(j))  # 2値化画像の読み込み
            kernel = np.ones((3, 3), np.uint8)
            img = cv2.dilate(im, kernel, iterations=1)  # 1ピクセル幅だけ白を増やす
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(img, 100, 255, 0)
            img, contours, hierarchy = cv2.findContours(thresh,
                                                        cv2.RETR_TREE,
                                                        cv2.CHAIN_APPROX_SIMPLE)  # エッジ検出

            # アノテーション生成
            if hierarchy is not None:
                num_of_an = int(hierarchy.size / 4)  # アノテーションの個数を算出する
            file = os.path.basename(file)
            # json内にファイルサイズを書く
            filesize = os.path.getsize('{}'.format(os.path.join(self.originaldir, file)))

            f.write('"{}'.format(file))  # まず画像の名前を書き出す
            f.write(str(filesize))
            f.write('":{"fileref":"","size":')
            f.write(str(filesize))
            f.write(',"filename":"{}","base64_img_data":"","file_attributes":'.format(file))
            f.write('{},"regions":{')

            if hierarchy is not None:
                for ii in range(num_of_an):     # アノテーションの個数分ループ
                    an_matrix = contours[ii][:, 0]  # ii番目のアノテーションのマトリックスを取り出す
                    f.write('"{0}":'.format(ii))  # ii番目のアノテーション文を書き始める
                    f.write('{"shape_attributes":{"name":"polygon",')

                    f.write('"all_points_x":')  # x座標に関するアノテーション文を書き始める
                    x_column = an_matrix[:, 0]  # 取り出したマトリックスのx座標に相当する列を取り出す
                    x_list = x_column.tolist()  # 取り出した列をリストに変換する
                    x_list.append(x_list[0])   # リストの先頭値をリストの最後に書き足してアノテーションを閉じた系にする
                    str_x_list = str(x_list)     # jsonファイルに書き込むためにリストを文字列化する
                    f.write(str_x_list)        # x座標をアノテーション文に書き込む

                    f.write(',"all_points_y":')   # y座標に関するアノテーション文を書き始める
                    y_column = an_matrix[:, 1]   # 取り出したマトリックスのy座標に相当する列を取り出す
                    y_list = y_column.tolist()  # 取り出した列をリストに変換する
                    y_list.append(y_list[0])   # リストの先頭値をリストの最後に書き足してアノテーションを閉じた系にする
                    str_y_list = str(y_list)   # jsonファイルに書き込むためにリストを文字列化する
                    f.write(str_y_list)        # y座標をアノテーション文に書き込む

                    f.write('},"region_attributes":')
                    f.write('{}}')
                    if ii != num_of_an-1:       # その画像におけるアノテーションが最後でなければカンマを打って続ける
                        f.write(',')
            f.write('}}')
            if j != len(files)-1:  # その画像が最後でなければカンマを打って続ける
                f.write(',')
            j += 1
        f.write('}')
        f.close()
