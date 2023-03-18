from lib.util import openImg
from PIL import Image
import numpy as np
import pyocr
import pyocr.builders
import time

tools = pyocr.get_available_tools()
tool = tools[0]

def getScore(url, psm):
  # timer start
  start = time.time()

  # read image from url(http) as numpy-array(RGB)
  img = openImg(url)

  # crop img
  # left:0 top:1/6 right:1/2 bottom:1/2 
  img = img[img.shape[0]//6 : img.shape[0]//2, 0 : img.shape[1]//2]

  # get time of do-preprocessing
  time_preprocess = time.time() - start
  start = time.time()

  # to grayscale
  for y in range(img.shape[0]):
    for x in range(img.shape[1]):
      r, g, b = img[y][x]

      if 225 <= r <= 255 and 55 <= g <= 115 and 140 <= b <= 200:
        color = 0
      else:
        color = 255

      img[y][x] = [color, color, color]
  
  # get time of do-grayscale
  time_grayscale = time.time() - start
  start = time.time()

  # validate psm-args
  # arrow '6' or '7' (else, using 6)
  if psm == '6' or psm == '7':
    # using psm from args as int(number)
    psm = int(psm)
  else:
    psm = 6

  # generate builder
  builder = pyocr.builders.DigitBuilder(tesseract_layout=psm)
  
  # do OCR
  result = tool.image_to_string(Image.fromarray(img), lang='eng', builder=builder)

  # get time of do-ocr
  time_ocr = time.time() - start

  # return result
  res = {
    'builder': 'DigitBuilder',
    'psm': str(psm),
    'time': {
      'preprocessing': time_preprocess,
      'grayscale': time_grayscale,
      'ocr': time_ocr
    },
    'result': result
  }

  return res
