from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from pydantic import Field, BaseModel

import models
from db import SessionLocal, engine
from sqlalchemy.orm import Session

from lib.score import getScore
from lib.difficult import getDifficult
from lib.title import getTitle
from lib.judge import getJudge

from lib.util import openImg, load_diff

from lib.candidate import candidateDifficult
from lib.candidate import candidateTitle

import requests
import json

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
    candidateRatio: float = Field(default=0.3)
    candidate: bool = Field(default=True)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
def get_music(db: Session = Depends(get_db)):
    music_db = db.query(models.Music).all()
    tmp = {}
    for m in music_db:
        tmp[m.id] = m
    return { "data": tmp }

@app.get("/get")
def get_new_data():
    # httpから取得
    music = json.loads(requests.get("https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/main/musics.json").text)
    difficult = json.loads(requests.get('https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/main/musicDifficulties.json').text)
    if load_diff(music=music, difficult=difficult):
        return { 'ok': False }

    try:
        # データの結合
        result = {}
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
            result[tmp["id"]] = tmp
    except:
        return { "ok": False }

    return { "ok": True, "data": result }

@app.get("/set-online")
def set_from_online(db: Session = Depends(get_db)):
    # httpから取得
    music = json.loads(requests.get("https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/main/musics.json").text)
    difficult = json.loads(requests.get('https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/main/musicDifficulties.json').text)

    if load_diff(music=music, difficult=difficult):
        return { 'ok': False }

    # データの結合
    result = []
    for m in music:
        tmp = {
            "id": m["id"],
            "title": m["title"] if m["title"] else None,
            "pronunciation": m["pronunciation"] if m["title"] else None,
            "creator": m["creator"] if m["creator"] else None,
            "lyricist": m["lyricist"] if m["lyricist"] else None,
            "composer": m["composer"] if m["composer"] else None,
            "arranger": m["arranger"] if m["arranger"] else None
        }       

        for d in difficult:
            if d["musicId"] == m["id"]:
                tmp["level_" + d["musicDifficulty"]] = d["playLevel"]
                tmp["totalNote_" + d["musicDifficulty"]] = d["totalNoteCount"]
        result.append(tmp)

    db.query(models.Music).delete()
    db.commit()

    for data in result:
        item = models.Music(
            id = data['id'],
            title = data['title'],
            pronunciation = data['pronunciation'],
            creator = data['creator'],
            lyricist = data['lyricist'],
            composer = data['composer'],
            arranger = data['arranger'],
            level_easy = data['level_easy'],
            level_normal = data['level_normal'],
            level_hard = data['level_hard'],
            level_expert = data['level_expert'],
            level_master = data['level_master'],
            totalNote_easy = data['totalNote_easy'],
            totalNote_normal = data['totalNote_normal'],
            totalNote_hard = data['totalNote_hard'],
            totalNote_expert = data['totalNote_expert'],
            totalNote_master = data['totalNote_master']
        )
        db.add(item)
    db.commit()

    return { "ok": True }
