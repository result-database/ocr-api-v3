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



    img3 = img.copy()
    img4 = img.copy()

    r, g, b = img4[:, :, 0], img4[:, :, 1], img4[:, :, 2]
    mask = np.logical_and.reduce((r >= 171 - border, r <= 171 + border, 
                                g >= 172 - border, g <= 172 + border, 
                                b >= 189 - border, b <= 189 + border))
    img4[mask] = [0, 0, 0]
    img4[np.logical_not(mask)] = [255, 255, 255]

    img4 = cv2.medianBlur(img4, 9)

    crop_range1 = Image.fromarray(img4).convert('RGB').getbbox()
    img4 = img4[crop_range1[1] : (crop_range1[3]) // 2, crop_range1[0] : crop_range1[2]]

    crop_range2 = Image.fromarray(img4).convert('RGB').getbbox()
    vertical_start = crop_range2[1] + (crop_range2[3] - crop_range2[1]) // 3
    vertical_end = crop_range2[1] + 2 * (crop_range2[3] - crop_range2[1]) // 3
    img4 = img4[vertical_start : vertical_end, crop_range2[0] : crop_range2[2]]

    img4 = 255 - img4

    crop_range3 = Image.fromarray(img4).convert('RGB').getbbox()
    img4 = img4[crop_range3[1] : crop_range3[3], crop_range3[0] : crop_range3[2]]

    h, w, _ = img3.shape

    img3 = img3[crop_range1[1]+vertical_start+crop_range3[3]+10 : -1, crop_range1[0]+crop_range2[0]+crop_range3[0]-0 : w]

    img5 = img3.copy()



    img5 = img3.copy()

    border = 20

    r, g, b = img5[:, :, 0], img5[:, :, 1], img5[:, :, 2]
    mask = np.logical_and.reduce((r >= 171 - border, r <= 171 + border, 
                                g >= 172 - border, g <= 172 + border, 
                                b >= 189 - border, b <= 189 + border))
    img5[mask] = [0, 0, 0]
    img5[np.logical_not(mask)] = [255, 255, 255]

    img5 = cv2.medianBlur(img5, 9)

    crop_range1 = Image.fromarray(img5).convert('RGB').getbbox()


    img6 = img3.copy()[crop_range1[1] : crop_range1[3], crop_range1[0] : crop_range1[2]]

    border = 225

    r, g, b = img6[:, :, 0], img6[:, :, 1], img6[:, :, 2]
    mask = np.logical_and(r >= border, np.logical_and(g >= border, b >= border))
    img6[mask] = [0, 0, 0]
    img6[np.logical_not(mask)] = [255, 255, 255]


    img6 = img6[0 : img6.shape[0], 0 : img6.shape[1] // 2]

    # get time of do-grayscale
    time_grayscale = time.time() - start
    start = time.time()

    # generate builder
    builder = pyocr.builders.TextBuilder(tesseract_layout=psm)
    builder.tesseract_configs.append('-c')
    builder.tesseract_configs.append('tessedit_char_whitelist="EASYNORMLHDXPTA"')

    # do OCR
    result = tool.image_to_string(Image.fromarray(img6), lang="eng", builder=builder)

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




