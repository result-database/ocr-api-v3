from lib.util import openImg
from PIL import Image
import numpy as np
import pyocr
import pyocr.builders
import time
import cv2

tools = pyocr.get_available_tools()
tool = tools[0]

def getTitle(img, psm, border):
    # # validate border
    # # arrow number (else, using 215)
    # if border.isdecimal():
    #     border = int(border)
    # else:
    #     border = 215

    # timer start
    start = time.time()

    # # read image from url(http) as numpy-array(RGB)
    # img = openImg(url)

    # crop img
    # left:0 top:0 right:1/2 bottom:6/7
    img = img[0 : img.shape[0] // 7, 0 : img.shape[1] // 2]

    # get time of do-preprocessing
    time_preprocess = time.time() - start
    start = time.time()

    # to grayscale
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    mask = np.logical_and(r >= border, np.logical_and(g >= border, b >= border))
    img[mask] = [255, 255, 255]
    img[np.logical_not(mask)] = [0, 0, 0]

    # get time of do-grayscale
    time_grayscale = time.time() - start
    start = time.time()

    # getbox -> crop
    crop_range = Image.fromarray(img).convert('RGB').getbbox()
    img = img[crop_range[1] : (crop_range[3]) // 2, crop_range[0] : crop_range[2]]

    # create margin
    img = cv2.copyMakeBorder(img, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=[0,0,0])  

    # 白背景に黒文字に変更
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    mask = np.logical_and(r == 255, np.logical_and(g == 255, b == 255))
    img[mask] = [0, 0, 0]
    img[np.logical_not(mask)] = [255, 255, 255]

    # # validate psm-args
    # # arrow '6' or '7' or '11' (else, using 11)
    # if psm == "6" or psm == "7" or psm == '11':
    #     # using psm from args as int(number)
    #     psm = int(psm)
    # else:
    #     psm = 11

    # generate builder
    builder = pyocr.builders.TextBuilder(tesseract_layout=psm)

    # do OCR
    result = tool.image_to_string(Image.fromarray(img), lang="jpn", builder=builder)

    # delete white space
    result = result.replace(' ', '')
    result = result.replace('\n', '')

    # get time of do-ocr
    time_ocr = time.time() - start

    # return result
    res = {
        "builder": "TextBuilder",
        "psm": str(psm),
        "time": {
            "preprocessing": time_preprocess,
            "grayscale": time_grayscale,
            "ocr": time_ocr,
        },
        "result": result,
    }

    return res
