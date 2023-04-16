from PIL import Image
import numpy as np
import pyocr
import pyocr.builders
import time

tools = pyocr.get_available_tools()
tool = tools[0]


def getDifficult(img, psm):
    # timer start
    start = time.time()

    # crop img
    # left:0 top:0 right:1/2 bottom:6/7
    img = img[0 : img.shape[0] // 7 * 1, 0 : img.shape[1] // 2]

    # get time of do-preprocessing
    time_preprocess = time.time() - start
    start = time.time()

    # to grayscale
    # ループを使わずに条件式を計算して処理を高速化
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]

    # 各条件に合致する部分を検出
    mask1 = np.logical_and(94 < r, np.logical_and(r < 175, np.logical_and(179 < g, np.logical_and(g < 255, np.logical_and(28 < b, b < 108)))))
    mask2 = np.logical_and(54 < r, np.logical_and(r < 134, np.logical_and(144 < g, np.logical_and(g < 224, np.logical_and(192 < b, b < 255)))))
    mask3 = np.logical_and(204 < r, np.logical_and(r < 255, np.logical_and(135 < g, np.logical_and(g < 215, np.logical_and(21 < b, b < 101)))))
    mask4 = np.logical_and(180 < r, np.logical_and(r < 255, np.logical_and(42 < g, np.logical_and(g < 122, np.logical_and(64 < b, b < 144)))))
    mask5 = np.logical_and(132 < r, np.logical_and(r < 212, np.logical_and(22 < g, np.logical_and(g < 102, np.logical_and(190 < b, b < 255)))))

    # 当てはまるところを更新
    mask_a = np.logical_or.reduce([mask1, mask2, mask3, mask4, mask5])
    img[mask_a] = [0, 0, 0]

    # 上記以外の部分を一括で更新
    mask_b = np.logical_not(np.logical_or.reduce([mask1, mask2, mask3, mask4, mask5]))
    img[mask_b] = [255, 255, 255]

    # get time of do-grayscale
    time_grayscale = time.time() - start
    start = time.time()

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




