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

def has_duplicates(seq):
    return len(seq) != len(set(seq))

# 全消ししてからdifficultとmusicの旧をDBに突っ込むrouting
@app.get('/set_test')
def set_test_data(db: Session = Depends(get_db)):
    db.query(models.Difficult).delete()
    db.commit()
    db.query(models.Music).delete()
    db.commit()

    music_json = requests.get('http://localhost:8080/static/data/old-music.json').text
    difficult_json = requests.get('http://localhost:8080/static/data/old-difficult.json').text
    use_music_items = ['id', 'title', 'pronunciation', 'creator', 'lyricist', 'composer', 'arranger']
    use_difficult_items = ['id', 'musicId', 'musicDifficulty', 'playLevel', 'totalNoteCount']

    for music in json.loads(music_json):
        target = ''
        for i in use_music_items:
            target += str(music[i])
        item = models.Music(
            id = music['id'],
            title = music['title'],
            pronunciation = music['pronunciation'],
            creator = music['creator'],
            lyricist = music['lyricist'],
            composer = music['composer'],
            arranger = music['arranger'],
            hash = sha256(target)
        )
        db.add(item)
    db.commit()

    for difficult in json.loads(difficult_json):
        target = ''
        for i in use_difficult_items:
            target += str(difficult[i])
        item = models.Difficult(
            id = difficult['id'],
            musicId = difficult['musicId'],
            musicDifficulty = difficult['musicDifficulty'],
            playLevel = difficult['playLevel'],
            totalNoteCount = difficult['totalNoteCount'],
            hash = sha256(target)
        )
        db.add(item)
    db.commit()

    return {}

@app.get("/music")
def get_music(db: Session = Depends(get_db)):

    # httpから取得
    music_json = requests.get('http://localhost:8080/static/data/music.json')

    # データの整形
    ids = []
    data = {}
    use_items = ['id', 'title', 'pronunciation', 'creator', 'lyricist', 'composer', 'arranger']
    for i in json.loads(music_json.text):
        target = ''
        data[i['id']] = {}
        for item in use_items:
            target += str(i[item])
            data[i['id']][item] = i[item]
        ids.append(i['id'])
        data[i['id']]['hash'] = sha256(target)

    # idの重複がないかバリデーション
    if has_duplicates(ids):
        return { 'ok':False }

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
    
    return diff


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
