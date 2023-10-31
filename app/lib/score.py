from PIL import Image
import numpy as np
import pyocr
import pyocr.builders
import time
import cv2

tools = pyocr.get_available_tools()
tool = tools[0]

def getScore(img, psm, blur):
    # timer start
    start = time.time()

    # crop img
    # left:0 top:1/6 right:1/2 bottom:1/2
    img = img[img.shape[0] // 6 : img.shape[0] // 2, 0 : img.shape[1] // 3 * 2]

    # get time of do-preprocessing
    time_preprocess = time.time() - start
    start = time.time()

    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]
    border = 20
    mask = np.logical_and.reduce((r >= 255 - border, r <= 255 + border, 
                                g >= 119 - border, g <= 119 + border, 
                                b >= 170 - border, b <= 170 + border))
    img2 = img.copy()
    img2[mask] = [0, 0, 0]
    img2[np.logical_not(mask)] = [255, 255, 255]


    # 余白作成とblur
    if blur:
        img2 = cv2.blur(img2, (3, 3))
    img = cv2.copyMakeBorder(img, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=[255,255,255])  

    # get time of do-grayscale
    time_grayscale = time.time() - start
    start = time.time()

    # generate builder
    builder = pyocr.builders.DigitBuilder(tesseract_layout=psm)

    # do OCR
    result = tool.image_to_string(Image.fromarray(img2), lang="eng", builder=builder)

    # get time of do-ocr
    time_ocr = time.time() - start

    # return result
    res = {
        "builder": "DigitBuilder",
        "psm": str(psm),
        "time": {
            "preprocessing": time_preprocess,
            "grayscale": time_grayscale,
            "ocr": time_ocr,
        },
        "result": result,
    }

    return res
