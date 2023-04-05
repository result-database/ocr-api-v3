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

def set_data(db):
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
