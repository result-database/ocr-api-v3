from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from reqtypes import ReqType
from starlette.middleware.cors import CORSMiddleware

from lib.score import getScore
from lib.difficult import getDifficult
from lib.title import getTitle
from lib.judge import getJudge
from lib.util import openImg
from lib.candidate import candidateDifficult, candidateTitle

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)

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
        'candidateTitle': candidateTitle(common["title"]["result"], request.candidateRatio),
        'candidateDifficult': candidateDifficult(common["difficult"]["result"])
    }

    return {**common, **candidate} if request.candidate else common

