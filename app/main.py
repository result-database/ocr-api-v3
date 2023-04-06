from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

from lib.score import getScore
from lib.difficult import getDifficult
from lib.title import getTitle
from lib.judge import getJudge

from lib.candidate import candidateDifficult
from lib.candidate import candidateTitle

from lib.validate import load_diff

import models
from db import SessionLocal, engine
from sqlalchemy.orm import Session

import requests
import json

from test_data import set_data

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

# 全消ししてからdifficultとmusicの旧をDBに突っ込むrouting
@app.get('/set_test')
def set_test_data(db: Session = Depends(get_db)):
    set_data(db)
    return {}

@app.get("/load_diff")
def get_music(db: Session = Depends(get_db)):
    # httpから取得
    music = json.loads(requests.get('http://localhost:8080/static/data/music.json').text)
    difficult = json.loads(requests.get('http://localhost:8080/static/data/difficult.json').text)

    if load_diff(music=music, difficult=difficult):
        return {'ok': False}

    # データの結合
    result = []
    for m in music:
        tmp = {
            "id": m["id"],
            "title": m["title"],
            "pronunciation": m["pronunciation"],
            "creator": m["creator"],
            "lyricist": m["lyricist"],
            "composer": m["composer"],
            "arranger": m["arranger"]
        }
        for d in difficult:
            if d["musicId"] == m["id"]:
                tmp["level_" + d["musicDifficulty"]] = d["playLevel"]
                tmp["totalNote_" + d["musicDifficulty"]] = d["totalNoteCount"]
        result.append(tmp)
    
    # hashの計算
    items = ['id', 'title', 'pronunciation', 'creator', 'lyricist', 'composer', 'arranger', "level_easy","level_normal","level_hard","level_expert","level_master","totalNote_easy","totalNote_normal","totalNote_hard","totalNote_expert","totalNote_master"]
    
    for j in range(len(result)):
        target = ''
        for i in items:
            target += str(result[j][i])
        result[j]['hash'] = sha256(target)
    
    # 整形
    data = {}
    for i in result:
        data[i["id"]] = i

    # DBから取得
    music_db = db.query(models.Music).all()

    # データの整形
    data2 = {}
    for i in music_db:
        data2[i.id] = i.toDict()

    # idの差分をとる
    diff = {
        "deleted": data2.keys() - data.keys(),
        "added": data.keys() - data2.keys(),
        "same": data.keys() & data2.keys(),
        "updated": []
    }

    # hashを確認
    for i in diff['same'].copy():
        if data[i]['hash'] != data2[i]['hash']:
            diff['updated'].append(i)
            diff['same'].remove(i)
    
    # 具体的なデータをin
    diff2 = {
        "deleted": [],
        "added": [],
        "updated": []
    }
    for i in diff['deleted']:
        diff2['deleted'].append(data2[i])
    for i in diff['added']:
        diff2['added'].append(data[i])
    for i in diff['updated']:
        diff2['updated'].append({'old': data2[i], 'new': data[i]})

    return diff2

@app.get('/apply_diff')
def apply_diff(url):
    return {'ok':True}

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
