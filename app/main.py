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

class ReqType(BaseModel):
    url: str = Field(default="http://localhost:8080/static/wide.png")
    psmScore: int = Field(default=6, enum=[6, 7])
    psmDifficult: int = Field(default=7, enum=[6, 7])
    psmTitle: int = Field(default=11, enum=[6, 7, 11])
    psmJudge: int = Field(default=6, enum=[6, 7])
    borderTitle: int = Field(default=215, ge=215, le=255)
    borderJudge: int = Field(default=230, ge=230, le=255)
    blurScore: bool = Field(default=True)
    blurDifficult: bool = Field(default=True)
    blurTitle: bool = Field(default=True)
    blurJudge: bool = Field(default=True)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post('/ocr/v2')
def ocr_v2(request: ReqType):
    # urlじゃなくてnd-arrayを送りつける
    img = openImg(request.url)
    return {
        'score': getScore(img.copy(), request.psmScore, request.blurScore), 
        'difficult': getDifficult(img.copy(), request.psmDifficult, request.blurDifficult), 
        'title': getTitle(img.copy(), request.psmTitle, request.blurTitle, request.borderTitle), 
        'judge': getJudge(img.copy(), request.psmJudge, request.blurJudge, request.borderJudge)
    }

@app.get("/set")
def set_sample_data():
    return { "ok": True }

@app.get('/candidate/difficult')
def candidate_difficult(data):
    return {'candidate': candidateDifficult(data)}

@app.get('/candidate/title')
def candidate_title(data, ratio):
    return {'candidate': candidateTitle(data, ratio)}
