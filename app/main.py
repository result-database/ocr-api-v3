from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from lib.score import getScore
from lib.difficult import getDifficult
from lib.title import getTitle
from lib.judge import getJudge

from lib.util import openImg

from lib.candidate import candidateDifficult
from lib.candidate import candidateTitle

from concurrent.futures import ProcessPoolExecutor
import asyncio

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/ocr/v1')
async def ocr_v1(url):
    img = openImg(url)
    def process_ocr_with_processes(img):
        with ProcessPoolExecutor() as executor:
            score = executor.submit(getScore, img.copy(), 'a')
            difficult = executor.submit(getDifficult, img.copy(), 'a')
            title = executor.submit(getTitle, img.copy(), 'a', 'a')
            judge = executor.submit(getJudge, img.copy(), 'a', 'a')

        return {'score': score.result(), 'difficult': difficult.result(), 'title': title.result(), 'judge':judge.result()}

    # 並列処理でOCRを実行して結果を返す
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, process_ocr_with_processes, img)
    return result

@app.get('/ocr/v2')
def ocr_v2(url):
    # urlじゃなくてnd-arrayを送りつける
    img = openImg(url)
    return {'score': getScore(img.copy(), "a"), 'difficult': getDifficult(img.copy(), "a"), 'title': getTitle(img.copy(), "a", "a"), 'judge': getJudge(img.copy(), "a", "a")}

@app.get('/candidate/difficult')
def candidate_difficult(data):
    return {'candidate': candidateDifficult(data)}

@app.get('/candidate/title')
def candidate_title(data, ratio):
    return {'candidate': candidateTitle(data, ratio)}
