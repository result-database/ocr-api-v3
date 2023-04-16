from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from PIL import Image
import numpy as np
import io

from lib.score import getScore
from lib.difficult import getDifficult
from lib.title import getTitle
from lib.judge import getJudge

from lib.candidate import candidateDifficult
from lib.candidate import candidateTitle

from concurrent.futures import ProcessPoolExecutor
import asyncio

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/ocr/v1')
async def ocr(url):
    def process_ocr_with_processes(url):
        with ProcessPoolExecutor() as executor:
            score = executor.submit(getScore, url, 'a')
            difficult = executor.submit(getDifficult, url, 'a')
            title = executor.submit(getTitle, url, 'a', 'a')
            judge = executor.submit(getJudge, url, 'a', 'a')

        return {'score': score.result(), 'difficult': difficult.result(), 'title': title.result(), 'judge':judge.result()}

    # 並列処理でOCRを実行して結果を返す
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, process_ocr_with_processes, url)
    return result

@app.get('/candidate/difficult')
def candidate_difficult(data):
    return {'candidate': candidateDifficult(data)}

@app.get('/candidate/title')
def candidate_title(data, ratio):
    return {'candidate': candidateTitle(data, ratio)}

@app.get('/ocr/title')
def title(url, psm, border):
    img = getTitle(url, psm, border)

    # NumPy 配列を Pillow の Image オブジェクトに変換する
    img_pil = Image.fromarray(img)
    img_pil = img_pil.convert("RGB")

    # Pillow の Image オブジェクトをバイナリストリームに変換する
    img_byteio = io.BytesIO()
    img_pil.save(img_byteio, format="JPEG")
    img_byteio.seek(0)

    # ストリーミングレスポンスを生成して画像を返す
    return StreamingResponse(
        content=img_byteio,
        media_type="image/jpeg"
    )