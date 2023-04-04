from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

from lib.score import getScore
from lib.difficult import getDifficult
from lib.title import getTitle
from lib.judge import getJudge

from lib.candidate import candidateDifficult
from lib.candidate import candidateTitle

import models, query
from db import SessionLocal, engine
from sqlalchemy.orm import Session

import requests
import json

from lib.sha256 import sha256

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def index(name:str):
    return {"message": "Hello,{}!".format(name)}

@app.get("/music")
def get_music(db: Session = Depends(get_db)):
    music_json = requests.get('http://localhost:8080/static/data/new-music.json')
    data = {}
    for i in json.loads(music_json.text):
        i.pop("seq")
        i.pop("releaseConditionId")
        i.pop("categories")
        i.pop("dancerCount")
        i.pop("selfDancerPosition")
        i.pop("assetbundleName")
        i.pop("liveTalkBackgroundAssetbundleName")
        i.pop("publishedAt")
        i.pop("liveStageId")
        i.pop("fillerSec")
        data[i["id"]] = sha256(i)
    print("ids: " + str(list(data.keys())))
    return data

@app.get("/difficult")
def get_difficult():
    difficult_json = requests.get('http://localhost:8080/static/data/new-difficult.json')
    musicIds = []
    data = {}
    for i in json.loads(difficult_json.text):
        musicIds.append(i["musicId"])

    for musicId in list(set(musicIds)):
        data[musicId] = []
    for i in json.loads(difficult_json.text):
        i.pop("releaseConditionId")
        data[i["musicId"]].append(sha256(i))

    return data

@app.get('/ocr/score')
def score(url, psm):
    return getScore(url, psm)

@app.get('/ocr/difficult') 
def difficult(url, psm):
    return getDifficult(url, psm)

@app.get('/ocr/title')
def title(url, psm, border):
    return getTitle(url, psm, border)

@app.get('/ocr/judge')
def judge(url, psm, border):
    return getJudge(url, psm, border)

@app.get('/candidate/difficult')
def candidate_difficult(data):
    return {'candidate': candidateDifficult(data)}

@app.get('/candidate/title')
def candidate_title(data, ratio):
    return {'candidate': candidateTitle(data, ratio)}
