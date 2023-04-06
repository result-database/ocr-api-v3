from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

from lib.score import getScore
from lib.difficult import getDifficult
from lib.title import getTitle
from lib.judge import getJudge

from lib.candidate import candidateDifficult
from lib.candidate import candidateTitle

import models
from db import SessionLocal, engine
from sqlalchemy.orm import Session

import requests
import json

from lib.sha256 import sha256

def set_data(db):
    db.query(models.Music).delete()
    db.commit()

    data_json = requests.get('http://localhost:8080/static/data/old-data.json').text
    items = ['id', 'title', 'pronunciation', 'creator', 'lyricist', 'composer', 'arranger', "level_easy","level_normal","level_hard","level_expert","level_master","totalNote_easy","totalNote_normal","totalNote_hard","totalNote_expert","totalNote_master"]

    for data in json.loads(data_json):
        target = ''
        for i in items:
            target += str(data[i])
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
            totalNote_master = data['totalNote_master'],
            hash = sha256(target)
        )
        db.add(item)
    db.commit()
