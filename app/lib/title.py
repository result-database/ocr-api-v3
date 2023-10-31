from PIL import Image
import numpy as np
import pyocr
import pyocr.builders
import time
import cv2
import math

tools = pyocr.get_available_tools()
tool = tools[0]

def getTitle(img, psm, blur, border2):
    # timer start
    start = time.time()

    # crop img
    # left:0 top:0 right:1/2 bottom:6/7
    img = img[0 : img.shape[0] // 7, 0 : img.shape[1] // 2]

    # get time of do-preprocessing
    time_preprocess = time.time() - start
    start = time.time()

    border = 10
    img2 = img.copy()

    r, g, b = img2[:, :, 0], img2[:, :, 1], img2[:, :, 2]
    mask = np.logical_and.reduce((r >= 171 - border, r <= 171 + border, 
                                g >= 172 - border, g <= 172 + border, 
                                b >= 189 - border, b <= 189 + border))
    img2[mask] = [255, 255, 255]
    img2[np.logical_not(mask)] = [0, 0, 0]

    img2 = cv2.medianBlur(img2, 9)

    crop_range = Image.fromarray(img2).convert('RGB').getbbox()
    img = img[crop_range[1] : (crop_range[3]) // 1, crop_range[0] : crop_range[2]]

    img2 = img.copy()[0 : math.floor(img2.shape[0] / 2), math.floor(img2.shape[1] / 6) : img2.shape[1]]
    # img2 = img.copy()[0 : math.floor(img2.shape[0] / 2), 0 : img2.shape[1]]

    border = 120

    r, g, b = img2[:, :, 0], img2[:, :, 1], img2[:, :, 2]
    mask = np.logical_and(r <= border, np.logical_and(g <= border, b <= border))
    img2[mask] = [0, 0, 0]
    img2[np.logical_not(mask)] = [255, 255, 255]

    # get time of do-grayscale
    time_grayscale = time.time() - start
    start = time.time()

    # generate builder
    builder = pyocr.builders.TextBuilder(tesseract_layout=psm)

    # do OCR
    result = tool.image_to_string(Image.fromarray(img2), lang="jpn", builder=builder)

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
