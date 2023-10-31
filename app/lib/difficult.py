from PIL import Image
import numpy as np
import pyocr
import pyocr.builders
import time
import cv2
import math

tools = pyocr.get_available_tools()
tool = tools[0]


def getDifficult(img, psm, blur):
    # timer start
    start = time.time()

    img = img[0 : img.shape[0] // 7, 0 : img.shape[1] // 2]
    
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

    img = img[math.floor(img.shape[0] / 2) : img.shape[0], math.floor(img.shape[1] / 4) : math.floor(img.shape[1] / 2)]

    border = 225

    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    mask = np.logical_and(r >= border, np.logical_and(g >= border, b >= border))
    img[mask] = [0, 0, 0]
    img[np.logical_not(mask)] = [255, 255, 255]


    # get time of do-grayscale
    time_grayscale = time.time() - start
    start = time.time()

    # generate builder
    builder = pyocr.builders.TextBuilder(tesseract_layout=psm)
    builder.tesseract_configs.append('-c')
    builder.tesseract_configs.append('tessedit_char_whitelist="EASYNORMLHDXPTA"')

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
            "grayscale": time_grayscale,
            "ocr": time_ocr,
        },
        "result": result,
    }

    return res




