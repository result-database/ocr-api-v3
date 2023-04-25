from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from reqtypes import ReqType, ReqType2

import models
from db import engine, get_db
from sqlalchemy.orm import Session

from lib.score import getScore
from lib.difficult import getDifficult
from lib.title import getTitle
from lib.judge import getJudge
from lib.util import openImg
from lib.candidate import candidateDifficult, candidateTitle
from lib.db_apply import apply
from lib.getdata import getFromOrigin, getFromDB

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post('/ocr/v2')
def ocr_v2(request: ReqType, db: Session = Depends(get_db)):
    # urlじゃなくてnd-arrayを送りつける
    img = openImg(request.url)
    
    common = {
        'score': getScore(img.copy(), request.psmScore, request.blurScore), 
        'difficult': getDifficult(img.copy(), request.psmDifficult, request.blurDifficult), 
        'title': getTitle(img.copy(), request.psmTitle, request.blurTitle, request.borderTitle), 
        'judge': getJudge(img.copy(), request.psmJudge, request.blurJudge, request.borderJudge)
    }

    candidate = {
        'candidateTitle': candidateTitle(common["title"]["result"], request.candidateRatio, db, models),
        'candidateDifficult': candidateDifficult(common["difficult"]["result"])
    }

    return {**common, **candidate} if request.candidate else common

@app.get("/music")
def get_from_db(db: Session = Depends(get_db)):
    return getFromDB(db=db, models=models)

@app.get("/get")
def get_from_origin():
    return getFromOrigin()

@app.post("/apply")
def apply_patch(request: ReqType2, db: Session = Depends(get_db)):
    return apply(models=models, db=db, request=request)
