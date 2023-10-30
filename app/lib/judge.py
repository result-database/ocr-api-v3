from lib.util import searchPosition
from PIL import Image
import numpy as np
import pyocr
import pyocr.builders
import time
import cv2
import math

tools = pyocr.get_available_tools()
tool = tools[0]

judges = ['PERFECT', 'GREAT', 'GOOD', 'BAD', 'MISS']
from_img = cv2.cvtColor(cv2.imread('./lib/template.png'), cv2.COLOR_BGR2RGB)

def getJudge(to_img, psm, blur, border):
    # timer start
    start = time.time()

    # generaet builder
    builder = pyocr.builders.DigitBuilder(tesseract_layout=psm)

    Mx, dst = searchPosition(templ_img=from_img, query_img=to_img)
    x, y = np.sort(dst[0,:,0]), np.sort(dst[0,:,1])
    img = to_img[y[0] : y[3] , x[3] : x[3] + math.floor((x[3] - x[0]) / 5 * 4)]

    # いろいろ定義
    datas = {}
    hight = img.shape[0] // 5

    # get time of do-prepare
    time_prepare = time.time() - start
    start = time.time()

    # core
    for i in range(len(judges)):
        cropped_img = img[hight * i : hight * (i + 1), 0 : img.shape[1]]

        # convert to grayscale
        r, g, b = cropped_img[:, :, 0], cropped_img[:, :, 1], cropped_img[:, :, 2]
        mask = np.logical_and(r >= border, np.logical_and(g >= border, b >= border))
        cropped_img[mask] = [0, 0, 0]
        cropped_img[np.logical_not(mask)] = [255, 255, 255]

        # 余白作成とblur
        if blur:
            cropped_img = cv2.blur(cropped_img, (3, 3))
        cropped_img = cv2.copyMakeBorder(cropped_img, 100, 100, 100, 100, cv2.BORDER_CONSTANT, value=[255,255,255])  

        result = tool.image_to_string(Image.fromarray(cropped_img), lang='eng', builder=builder)
        datas[judges[i]] = result


    # get time of do-ocr
    time_ocr = time.time() - start

    # return result
    res = {
        "builder": "DigitBuilder",
        "psm": str(psm),
        "time": {
            "prepare": time_prepare,
            "ocr": time_ocr
        },
        "result": datas,
    }

    return res
