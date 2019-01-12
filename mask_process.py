# coding=utf-8
import cv2
import os
import  numpy as np
from  skimage.measure import label
SRC_PATH ="C:\Learning\CV\Video\output\Mymask"
DST_PATH="C:\Learning\CV\Video\output\MaskProcessed"
IMG_FORMAT = [".jpg",".png"]

def  opening(image):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # binary = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    binary = cv2.dilate(image,kernel,iterations = 1)
    return  binary

def find_max(bw_img):

    labeled_img, num = label(bw_img, connectivity =2, background=0, return_num=True)
    # plt.figure(), plt.imshow(labeled_img, 'gray')

    # print  labeled_img
    max_label = 0
    max_num = 0
    for i in range(1, num):  # 这里从1开始，防止将背景设置为最大连通域
        if np.sum(labeled_img == i) > max_num:
            # print  i
            max_num = np.sum(labeled_img == i)
            max_label = i
    lcc = (labeled_img == max_label)
    lcc=lcc.astype(np.uint8)
    lcc *= 255
    return lcc






def process(src,formats,img_save_path):
    imgs = os.listdir(src)

    def filter_format(x, all_formats):
        if x[-4:] in all_formats:
            return True
        else:
            return False

    imgs = filter(lambda x: filter_format(x, formats), imgs)
    if (not os.path.exists(img_save_path)):
        os.makedirs(img_save_path)

    for each_img in imgs:


        each_img_name = each_img[:-4]
        if each_img_name.find("fore")>=0:
            print ""
            continue
        print "正在读取图片：", each_img
        each_img_save_full_path = os.path.join(img_save_path, each_img_name)
        each_img_save_full_path.replace('\\', '/')
        each_img_full_path = os.path.join(src, each_img)
        each_img_full_path.replace('\\', '/')

        img = cv2.imread(each_img_full_path)
        res = find_max(img)
        res = opening(res)

        cv2.imwrite(each_img_save_full_path+".jpg", res)

if __name__ == '__main__':
    process(SRC_PATH,IMG_FORMAT,DST_PATH)