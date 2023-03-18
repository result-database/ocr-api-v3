from PIL import Image
import requests
import io
import numpy as np

def openImg(url):
  pil_img = Image.open(io.BytesIO(requests.get(url).content))
  return np.array(pil_img)
