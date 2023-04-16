from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import Field, BaseModel

from lib.score import getScore
from lib.difficult import getDifficult
from lib.title import getTitle
from lib.judge import getJudge

from lib.util import openImg

from lib.candidate import candidateDifficult
from lib.candidate import candidateTitle

from concurrent.futures import ProcessPoolExecutor
import asyncio

class ReqType(BaseModel):
    url: str
    psmScore: int = Field(default=6, enum=[6, 7])
    psmDifficult: int = Field(default=7, enum=[6, 7])
    psmTitle: int = Field(default=11, enum=[6, 7, 11])
    psmJudge: int = Field(default=6, enum=[6, 7])
    borderTitle: int = Field(default=215, ge=215, le=255)
    borderJudge: int = Field(default=230, ge=230, le=255)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post('/ocr/v1')
async def ocr_v1(request: ReqType):
    img = openImg(request.url)
    def process_ocr_with_processes(img):
        with ProcessPoolExecutor() as executor:
            score = executor.submit(getScore, img.copy(), request.psmScore)
            difficult = executor.submit(getDifficult, img.copy(), request.psmDifficult)
            title = executor.submit(getTitle, img.copy(), request.psmTitle, request.borderTitle)
            judge = executor.submit(getJudge, img.copy(), request.psmJudge, request.borderJudge)

        return {'score': score.result(), 'difficult': difficult.result(), 'title': title.result(), 'judge':judge.result()}

    # 並列処理でOCRを実行して結果を返す
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, process_ocr_with_processes, img)
    return result

@app.post('/ocr/v2')
def ocr_v2(request: ReqType):
    # urlじゃなくてnd-arrayを送りつける
    img = openImg(request.url)
    return {
        'score': getScore(img.copy(), request.psmScore), 
        'difficult': getDifficult(img.copy(), request.psmDifficult), 
        'title': getTitle(img.copy(), request.psmTitle, request.borderTitle), 
        'judge': getJudge(img.copy(), request.psmJudge, request.borderJudge)
    }

@app.get('/candidate/difficult')
def candidate_difficult(data):
    return {'candidate': candidateDifficult(data)}

@app.get('/candidate/title')
def candidate_title(data, ratio):
    return {'candidate': candidateTitle(data, ratio)}
