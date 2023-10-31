from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from reqtypes import ReqType, ReqType2

from lib.score import getScore
from lib.difficult import getDifficult
from lib.title import getTitle
from lib.judge import getJudge
from lib.util import openImg
from lib.candidate import candidateDifficult, candidateTitle

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post('/ocr/v3')
def ocr_v3(request: ReqType):
    # urlじゃなくてnd-arrayを送りつける
    img = openImg(request.url)
    
    common = {
        'score': getScore(img.copy(), request.psmScore, request.blurScore), 
        'difficult': getDifficult(img.copy(), request.psmDifficult, request.blurDifficult), 
        'title': getTitle(img.copy(), request.psmTitle, request.blurTitle, request.borderTitle), 
        'judge': getJudge(img.copy(), request.psmJudge, request.blurJudge, request.borderJudge)
    }

    candidate = {
        # 'candidateTitle': candidateTitle(common["title"]["result"], request.candidateRatio),
        # 'candidateDifficult': candidateDifficult(common["difficult"]["result"])
    }

    return {**common, **candidate} if request.candidate else common

