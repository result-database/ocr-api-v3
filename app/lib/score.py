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
    img = img[img.shape[0] // 6 : img.shape[0] // 2, 0 : img.shape[1] // 2]

    # get time of do-preprocessing
    time_preprocess = time.time() - start
    start = time.time()

    # to grayscale
    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]
    mask = np.logical_and(225 <= r, np.logical_and(r <= 255, np.logical_and(55 <= g, np.logical_and(g <= 115, np.logical_and(140 <= b, b <= 200)))))

    # 一括で更新
    img[mask] = [0, 0, 0]
    img[np.logical_not(mask)] = [255, 255, 255]

    # 余白作成とblur
    if blur:
        img = cv2.blur(img, (3, 3))
    img = cv2.copyMakeBorder(img, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=[255,255,255])  

    # get time of do-grayscale
    time_grayscale = time.time() - start
    start = time.time()

    # generate builder
    builder = pyocr.builders.DigitBuilder(tesseract_layout=psm)

    # do OCR
    result = tool.image_to_string(Image.fromarray(img), lang="eng", builder=builder)

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
