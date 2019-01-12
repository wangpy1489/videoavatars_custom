# coding=utf-8

import os
import cv2
import  base64
import requests
import numpy as np

SRC_PATH ="C:\Learning\CV\Video2\output\Myvideo"
DST_PATH="C:\Learning\CV\Video2\output\Mymask"
IMG_FORMAT = [".jpg",".png"]
ACC_KEY="t2NNFAo81BtzKLOGWFsOLal2"
SECRET_KEY="9MHfuf1qUpcgpmNU1WeMKKxja5sp4Dpx"
WIDTH =1080
HEIGHT = 1080

def get_access(acc_key,secret_key):
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+acc_key+'&client_secret='+secret_key
    headers ={'Content-Type': 'application/json; charset=UTF-8'}
    res = requests.post(host,headers=headers)
    response = res.json()
    return  response["access_token"]

def img_base64(img_src):
    # b64encode是编码，b64decode是解码
    base64_data = ""
    with open(img_src,"rb") as f:
        base64_data = base64.b64encode(f.read())
        print "编码"+img_src
    return  base64_data


def base64_img(res,dst):
    labeldst = dst+"_label.jpg"
    foredst = dst + "_fore.jpg"
    with open(foredst, 'wb') as f:
        f.write(base64.b64decode(res["foreground"]))
        print "解码完毕"

    labelmap = base64.b64decode(res['labelmap'])  # res为通过接口获取的返回json
    nparr = np.fromstring(labelmap, np.uint8)
    labelimg = cv2.imdecode(nparr, 1)
    # width, height为图片原始宽、高
    labelimg = cv2.resize(labelimg, (WIDTH, HEIGHT), interpolation=cv2.INTER_NEAREST)
    im_new = np.where(labelimg == 1, 255, labelimg)
    cv2.imwrite(labeldst, im_new)

def human_mask(src,formats,img_save_path):
    imgs = os.listdir(src)

    def filter_format(x, all_formats):
        if x[-4:] in all_formats:
            return True
        else:
            return False

    imgs = filter(lambda x: filter_format(x, formats), imgs)
    if (not os.path.exists(img_save_path)):
        os.makedirs(img_save_path)
    access_token =get_access(ACC_KEY,SECRET_KEY)

    for each_img in imgs:
        print "正在读取图片：", each_img

        each_img_name = each_img[:-4]
        each_img_save_full_path = os.path.join(img_save_path, each_img_name)
        each_img_save_full_path.replace('\\','/')
        each_img_full_path = os.path.join(src, each_img)
        each_img_full_path.replace('\\', '/')

        each_img_base64 = img_base64(each_img_full_path)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        param ={"image":each_img_base64}
        res = requests.post("https://aip.baidubce.com/rest/2.0/image-classify/v1/body_seg?access_token="+access_token,
                            headers=headers,
                            data=param)
        response = res.json()
        base64_img(response,each_img_save_full_path)
        

if __name__ == '__main__':
    human_mask(SRC_PATH, IMG_FORMAT, DST_PATH)

