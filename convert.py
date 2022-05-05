import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QSlider
from PyQt5 import QtCore

import argparse
import os
import cv2
import copy
import time
import numpy as np

class image_utils:
    
    def median_filter(self, src, ksize):
        d = int((ksize-1)/2)
        h, w = src.shape[0], src.shape[1]

        dst = src.copy()

        for y in range(d, h - d):
            for x in range(d, w - d):
                dst[y][x] = np.median(src[y-d:y+d+1, x-d:x+d+1])
        return dst

    def export_edges(self, image: np.ndarray, depth_image: np.ndarray, threshold: int = 150):
        cv2.imwrite("depth_image.png", depth_image)

        depth_image = depth_image[:,:,0]
        mask = depth_image > threshold
        # maskを二値化
        mask = mask.astype(np.uint8) * 255

        # imageとmaskの合成
        result = cv2.bitwise_and(image, image, mask=mask)
        result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        # メディアンフィルタ
        result = self.median_filter(result, ksize=5)
        # Canny輪郭検出
        edges = cv2.Canny(result, 199, 200)
        # MorphologyEx
        kernel = np.ones((5, 5), np.uint8)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        edges = cv2.morphologyEx(edges, cv2.MORPH_GRADIENT, kernel)

        # 反転
        edges = cv2.bitwise_not(edges)
        edges = edges.astype(np.uint8) * 255 * 255
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        return edges

class App(QWidget):

    def getargs(self):
        # get argment
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--image-path', help='image folder path')
        parser.add_argument('-d', '--depth-path', help='image folder path')
        args = parser.parse_args()

        self.image_path = args.image_path
        self.depth_path = args.depth_path

        # get abs
        self.image_path = os.path.abspath(self.image_path)
        self.depth_path = os.path.abspath(self.depth_path)

        # not args
        if self.image_path is None:
            # exit
            sys.exit(0)

        if self.depth_path is None:
            # exit
            sys.exit(0)

    def load_images(self, _img_path=None, _depth_path=None):
        self.img_wide = cv2.imread(_img_path)
        self.img_d_wide = cv2.imread(_depth_path)

        img = copy.deepcopy(self.img_wide)
        img_d = copy.deepcopy(self.img_d_wide)

        w_h = img.shape[1] / img.shape[0]

        self.width = 600
        self.height = int(self.width / w_h)

        img = cv2.resize(img, (self.width, self.height))
        img_d = cv2.resize(img_d, (self.width, self.height))

        self.image_raw = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.image_depth = cv2.cvtColor(img_d, cv2.COLOR_BGR2RGB)

    def __init__(self):
        super().__init__()
        self.getargs()

        self.title = 'depth2line'
        self.th_count = 100
        self.left = 10
        self.top = 10

        self.geometry_w = 500
        self.geometry_h = 100

        self.initUI()

        self.load_images(self.image_path, self.depth_path)

    def depth_threshold(self):
        threshold = self.th_count
        print(threshold)

        # deep copy image_raw to image_raw_copy
        image_raw_copy = copy.deepcopy(self.image_raw)
        image_depth_copy = copy.deepcopy(self.image_depth)

        image_th_depth = cv2.cvtColor(image_depth_copy, cv2.COLOR_BGR2GRAY)
        image_th_depth = cv2.threshold(
            image_th_depth, threshold, 255, cv2.THRESH_BINARY)[1]
        image_raw_copy = cv2.bitwise_and(
            image_raw_copy, image_raw_copy, mask=image_th_depth)
        image_raw_copy = cv2.cvtColor(image_raw_copy, cv2.COLOR_BGR2RGB)

        cv2.imshow("image", image_raw_copy)
        cv2.waitKey(0)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(10, 10, self.geometry_w, self.geometry_h)

        # put slider -------------------------------------------------
        self.slider = QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setGeometry(0, 0, self.geometry_w, 20)

        self.slider.setMaximum(255)
        self.slider.setMinimum(0)
        self.slider.setValue(150)

        # slider event
        self.slider.valueChanged.connect(self.slider_event)

        # add button (conversion) ---------------------------------------
        self.button = QPushButton('conversion', self)
        # x: center y: under
        self.button.setGeometry(
            self.geometry_w//2 - 200, self.geometry_h - 30, self.geometry_w//2 - 100, 30)
        self.button.clicked.connect(self.conversion_event)

        self.show()

    def slider_event(self):
        time.sleep(0.01)
        self.th_count = self.slider.value()
        try:
            self.depth_threshold()
        except:
            print("error")
        # self.show()

    def conversion_event(self):
        print("detect: ", self.th_count)
        image_utils_class = image_utils()

        image = image_utils_class.export_edges(self.img_wide, self.img_d_wide, self.th_count)
        cv2.imwrite("edges_check.jpg", image)
        print("----- convert done -----")
        image_png = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
        for i in range(image_png.shape[0]):
            for j in range(image_png.shape[1]):
                if image_png[i][j][0] == 255 and image_png[i][j][1] == 255 and image_png[i][j][2] == 255:
                    image_png[i][j][3] = 0
                else:
                    image_png[i][j][0] = 255
                    image_png[i][j][1] = 200
                    image_png[i][j][2] = 255
                    image_png[i][j][3] = 180
        # export to png
        cv2.imwrite("edges.png", image_png)
        print("----- export done -----")
        print("----- You can close this GUI -----")
        # close
        cv2.destroyAllWindows()
        sys.exit(0)

    # close event
    def closeEvent(self, event):
        cv2.destroyAllWindows()
        print("close")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
