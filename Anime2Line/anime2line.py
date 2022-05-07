# © 2022 Ar-Ray-code (GPL-3.0 license)
import cv2
import numpy as np
import argparse
import sys

class image_utils:
    def median_filter(self, src, ksize):
        d = int((ksize-1)/2)
        h, w = src.shape[0], src.shape[1]
        dst = src.copy()

        for y in range(d, h - d):
            for x in range(d, w - d):
                dst[y][x] = np.median(src[y-d:y+d+1, x-d:x+d+1])
        return dst

    def export_edges_anime(self, image_raw: np.ndarray, depth_data: np.ndarray, median_ksize: int = 3, morph_g_ksize: int = 3, depth_threshold: int = 150, canny_threshold: int = 150):
        mask = depth_data > depth_threshold
        # maskを二値化
        mask = mask.astype(np.uint8) * 255
        # imageとmaskの合成
        result = cv2.bitwise_and(image_raw, image_raw, mask=mask)

        return self.anime2line(result, median_ksize=median_ksize, morph_g_ksize=morph_g_ksize, threshold=canny_threshold)

    def anime2line(self, image_raw: np.ndarray, median_ksize: int = 3, morph_g_ksize: int = 3, threshold: int = 150):
        edges = cv2.cvtColor(image_raw, cv2.COLOR_BGR2GRAY)

        # Canny輪郭検出
        edges = cv2.Canny(edges, threshold, threshold)

        # MorphologyEx
        if morph_g_ksize == 1:
            pass
        else:
            kernel_giant = np.ones((morph_g_ksize, morph_g_ksize), np.uint8)
            edges = cv2.morphologyEx(edges, cv2.MORPH_GRADIENT, kernel_giant)

        # 色の反転
        edges = cv2.bitwise_not(edges)
        edges = edges.astype(np.uint8) * 255 * 255
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # メディアンフィルタ
        if median_ksize == 1:
            pass
        else:
            edges = self.median_filter(edges, ksize=median_ksize)

        return edges

    # 白を透明にして色付きを半透明の白にする
    def white2transparent(self, input_image: np.ndarray, os_type: str = 'Ubuntu'):
        if os_type == 'Ubuntu':
            image_png = cv2.cvtColor(input_image, cv2.COLOR_RGB2RGBA)
            for i in range(image_png.shape[0]):
                for j in range(image_png.shape[1]):
                    if image_png[i][j][0] == 255 and image_png[i][j][1] == 255 and image_png[i][j][2] == 255:
                        image_png[i][j][3] = 0
                    else:
                        image_png[i][j][0] = 255
                        image_png[i][j][1] = 200
                        image_png[i][j][2] = 255
                        image_png[i][j][3] = 200
        elif os_type == 'Windows':
            image_png = cv2.cvtColor(input_image, cv2.COLOR_RGB2RGBA)
            for i in range(image_png.shape[0]):
                for j in range(image_png.shape[1]):
                    if image_png[i][j][0] == 255 and image_png[i][j][1] == 255 and image_png[i][j][2] == 255:
                        image_png[i][j][3] = 0
                    else:
                        image_png[i][j][0] = 200
                        image_png[i][j][1] = 255
                        image_png[i][j][2] = 255
                        image_png[i][j][3] = 200
        elif os_type == 'Mac-White':
            image_png = cv2.cvtColor(input_image, cv2.COLOR_RGB2RGBA)
            for i in range(image_png.shape[0]):
                for j in range(image_png.shape[1]):
                    if image_png[i][j][0] == 255 and image_png[i][j][1] == 255 and image_png[i][j][2] == 255:
                        image_png[i][j][3] = 0
                    else:
                        image_png[i][j][0] = 200
                        image_png[i][j][1] = 200
                        image_png[i][j][2] = 200
                        image_png[i][j][3] = 200
        elif os_type == 'Mac-Gray':
            image_png = cv2.cvtColor(input_image, cv2.COLOR_RGB2RGBA)
            for i in range(image_png.shape[0]):
                for j in range(image_png.shape[1]):
                    if image_png[i][j][0] == 255 and image_png[i][j][1] == 255 and image_png[i][j][2] == 255:
                        image_png[i][j][3] = 0
                    else:
                        image_png[i][j][0] = 70
                        image_png[i][j][1] = 70
                        image_png[i][j][2] = 70
                        image_png[i][j][3] = 200
        else:
            print("cannot detect wallpaper OS")
        return image_png

if __name__ == '__main__':
    image_utils = image_utils()
    # argparse
    parser = argparse.ArgumentParser(description='Anime2line argment')
    parser.add_argument('-i', '--image', type=str, help='input image')
    parser.add_argument('-km', '--kernel-median', type=int, help='kernel size of median filter', default=1)
    parser.add_argument('-kg', '--kernel-morph-giant', type=int, help='kernel size of morphologyEx giant', default=3)
    parser.add_argument('-t', '--threshold', type=int, help='threshold of Canny', default=150)
    parser.add_argument('-o', '--output', type=str, help='output image', default='output.png')

    args = parser.parse_args()
    if args.image is None:
        print("input image is not specified")
        sys.exit()
    else:
        image_raw = cv2.imread(args.image)

    median_ksize = args.kernel_median
    morph_g_ksize = args.kernel_morph_giant
    threshold = args.threshold
    output_image = args.output

    print("")
    print("---> Anime2line by Ar-Ray <---")
    print("------------------------------")
    print("Input image: " + args.image)
    print("median_ksize:", median_ksize)
    print("morph_g_ksize:", morph_g_ksize)
    print("threshold:", threshold)
    print("------------------------------")
    print("")
    
    image_raw = image_utils.anime2line(image_raw, median_ksize=median_ksize, morph_g_ksize=morph_g_ksize, threshold=threshold)

    cv2.imwrite(output_image, image_raw)
    print("output image is saved as " + output_image)