from PIL import Image
import requests
import io
import numpy as np
import cv2
import math

def is_float(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True

def openImg(url):
    pil_img = Image.open(io.BytesIO(requests.get(url).content))
    return np.array(pil_img)

def bubble_sort(arr):
    # ただのソート
    change = True
    while change:
        change = False
        for i in range(len(arr) - 1):
            if arr[i].distance > arr[i + 1].distance:
                arr[i].distance, arr[i + 1].distance = arr[i + 1].distance, arr[i].distance
                change = True
    return arr

def sort_for_difficult(arr):
    # ただのソート
    change = True
    while change:
        change = False
        for i in range(len(arr) - 1):
            if arr[i]['credibility'] < arr[i + 1]['credibility']:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                change = True
    return arr

def get_distance(x1, y1, x2, y2):
    # 二点間の距離を三平方の定理で求める
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return d

# search_contentとsearch_targetはRGBのNumpyArray
def get_ratio(search_content, search_target):
    # 特徴点の検出
    akaze = cv2.AKAZE_create()                                
    kp1, des1 = akaze.detectAndCompute(cv2.cvtColor(search_content,cv2.COLOR_BGR2GRAY) , None)
    kp2, des2 = akaze.detectAndCompute(cv2.cvtColor(search_target,cv2.COLOR_BGR2GRAY) , None)

    # 特徴点のマッチング
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # 特徴点の間引き
    ratio = 0.75
    good2 = []
    for m, n in matches:
        if m.distance < ratio * n.distance:
            good2.append(m)

    # 精度順にソートして、距離を求めて、倍率を出す
    good2 = bubble_sort(good2)

    distance_content = get_distance(
        x1=kp1[good2[0].queryIdx].pt[0],
        y1=kp1[good2[0].queryIdx].pt[1],
        x2=kp1[good2[1].queryIdx].pt[0],
        y2=kp1[good2[1].queryIdx].pt[1]
    )
    distance_target = get_distance(
        x1=kp2[good2[0].trainIdx].pt[0],
        y1=kp2[good2[0].trainIdx].pt[1],
        x2=kp2[good2[1].trainIdx].pt[0],
        y2=kp2[good2[1].trainIdx].pt[1]
    )

    # Magnification factor to match DPI
    return {'search_content': 1, 'search_target': 1 / (distance_target / distance_content)}

def match(face_img, full_img):
    # 2つの画像をマッチングする
    result = cv2.matchTemplate(full_img, face_img, cv2.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)

    tl = maxLoc
    br = (tl[0] + face_img.shape[1], tl[1] + face_img.shape[0])

    return tl, br

def grayscale(dst, color_range):
    # 例の青緑色を黒,それ以外を白にして出力する
    np_dst = np.full((dst.shape[0], dst.shape[1]), 0)


    r, g, b = dst[:, :, 0], dst[:, :, 1], dst[:, :, 2]
    mask1 = (r <= 70) & (215 <= g) & (g <= 255) & (205 <= b) & (b <= 236)
    mask2 = (114 - color_range < r) & (r < 144 + color_range) & (241 - color_range < g) & (g < 241 + color_range) & (219 - color_range < b) & (b < 219 + color_range)
    mask3 = (108 - color_range < r) & (r < 108 + color_range) & (193 - color_range < g) & (g < 193 + color_range) & (190 - color_range < b) & (b < 190 + color_range)
    mask4 = (115 - color_range < r) & (r < 115 + color_range) & (233 - color_range < g) & (g < 233 + color_range) & (215 - color_range < b) & (b < 215 + color_range)

    a = np.where(mask1 | mask2 | mask3 | mask4, 0, 255)

    np_dst = a[..., np.newaxis]

    return np_dst

def black_line(np_dst, search_target_ratio):
    # 縦のすべての列が黒の地点のx座標を調べる
    # 縦方向の列の合計を計算する
    col_sum = np_dst.sum(axis=0)

    # col_sum において、値が 0 であるインデックスを取得する
    black_cols = np.where(col_sum == 0)[0]

    # 黒い列のx座標を計算する
    black_cols = (black_cols * (1 / search_target_ratio)).astype(np.int64)

    return black_cols

class Ratio:
    def __init__(self, ratio, full_hight, tl, br):
        self.ratio = ratio
        self.hight = full_hight // 2
        self.top = self.restore(tl[1]) + self.hight
        self.bottom = self.restore(br[1]) + self.hight
    
    def restore(self, num):
        return math.floor(num * self.ratio)

def get_point(face_img, full_img):
    full_img_shape = full_img.shape

    # 変なところに特徴点がプロットされないように,なるべく小さくしておく
    full_img = full_img[
        full_img.shape[0] // 2 : full_img.shape[0] // 8 * 7,
        0 : full_img.shape[1] // 4 * 3
    ]

    # 検索内容が全体より大きくならないように縮小
    if full_img.shape[0] <= face_img.shape[0]:
        search_content_ratio = 1 - (face_img.shape[0] - full_img.shape[0]) / face_img.shape[0]
    else:
        search_content_ratio = 1
    face_img = cv2.resize(face_img, None, None, search_content_ratio, search_content_ratio)

    # DPIを揃えるための比と,戻すための比
    search_target_ratio = get_ratio(search_content=face_img, search_target=full_img)['search_target']
    full_ratio = 1 / search_target_ratio

    # DPIを揃える
    full_img = cv2.resize(full_img, None, None, search_target_ratio, search_target_ratio)

    # マッチングをする
    tl, br = match(face_img=face_img, full_img=full_img)

    # 緑線検出をする(crop -> grayscale -> get_position)
    dst = full_img.copy()
    dst = dst[
        tl[1] + face_img.shape[0] // 10 * 3 - 5 : tl[1] + face_img.shape[0] // 10 * 3 + 5,
        tl[0] : dst.shape[1]
    ]
    np_dst = grayscale(dst=dst, color_range=25)
    result = black_line(np_dst=np_dst, search_target_ratio=search_target_ratio)

    # 拡大を戻すいろいろ
    a = Ratio(ratio=full_ratio, full_hight=full_img_shape[0], tl=tl, br=br)

    # crop,search_target_ratioを配慮して座標を計算する
    final = { 'top': a.top, 'bottom': a.bottom, 'left': a.restore(br[0]), 'right': a.restore(tl[0]) + result[0] - 5 }

    return final
