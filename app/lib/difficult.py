from lib.util import openImg
from PIL import Image
import numpy as np
import pyocr
import pyocr.builders
import time

tools = pyocr.get_available_tools()
tool = tools[0]


def getDifficult(url, psm):
    # timer start
    start = time.time()

    # read image from url(http) as numpy-array(RGB)
    img = openImg(url)

    # crop img
    # left:0 top:0 right:1/2 bottom:6/7
    img = img[0 : img.shape[0] // 7 * 1, 0 : img.shape[1] // 2]

    # get time of do-preprocessing
    time_preprocess = time.time() - start
    start = time.time()

    # to grayscale
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            r, g, b = img[y][x]

            if 94 < r < 175 and 179 < g < 255 and 28 < b < 108:
                color = 0
            elif 54 < r < 134 and 144 < g < 224 and 192 < b < 255:
                color = 0
            elif 204 < r < 255 and 135 < g < 215 and 21 < b < 101:
                color = 0
            elif 180 < r < 255 and 42 < g < 122 and 64 < b < 144:
                color = 0
            elif 132 < r < 212 and 22 < g < 102 and 190 < b < 255:
                color = 0
            else:
                color = 255
            
            img[y][x] = [color, color, color]

    # get time of do-grayscale
    time_grayscale = time.time() - start
    start = time.time()

    # validate psm-args
    # arrow '6' or '7' (else, using 7)
    if psm == "6" or psm == "7":
        # using psm from args as int(number)
        psm = int(psm)
    else:
        psm = 7

    # generate builder
    builder = pyocr.builders.TextBuilder(tesseract_layout=psm)
    builder.tesseract_configs.append('-c')
    builder.tesseract_configs.append('tessedit_char_whitelist="EASYNORMLHDXPT"')

    # do OCR
    result = tool.image_to_string(Image.fromarray(img), lang="eng", builder=builder)

    # delete white space
    result = result.replace(' ', '')
    result = result.replace('\n', '')

    # get time of do-ocr
    time_ocr = time.time() - start

    # return result
    res = {
        "builder": "TextBuilder + whitelist",
        "psm": str(psm),
        "time": {
            "preprocessing": time_preprocess,
            "grayscale": time_grayscale,
            "ocr": time_ocr,
        },
        "result": result,
    }

    return res




