from lib.util import openImg
from lib.util import get_point
from PIL import Image
import numpy as np
import pyocr
import pyocr.builders
import time
import cv2

tools = pyocr.get_available_tools()
tool = tools[0]

judges = ['PERFECT', 'GREAT', 'GOOD', 'BAD', 'MISS']
search_content = cv2.cvtColor(cv2.imread('./lib/template.png'), cv2.COLOR_BGR2RGB)

def getJudge(img, psm, border):
    # timer start
    start = time.time()
    
    # validate border
    # arrow number (else, using 230)
    if border.isdecimal():
        border = int(border)
    else:
        border = 230

    # validate psm-args
    # arrow '6' or '7' (else, using 6)
    if psm == "6" or psm == "7":
        # using psm from args as int(number)
        psm = int(psm)
    else:
        psm = 6

    # generaet builder
    builder = pyocr.builders.DigitBuilder(tesseract_layout=psm)

    # # read image from url(http) as numpy-array(RGB)
    # search_target = openImg(url)
    search_target = img

    # judgeの座標を取得
    point = get_point(face_img=search_content, full_img=search_target)

    # crop img
    img = search_target[point['top'] : point['bottom'], point['left'] : point['right']]

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
        cropped_img[mask] = [0, 0, 2505]
        cropped_img[np.logical_not(mask)] = [255, 255, 255]

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
