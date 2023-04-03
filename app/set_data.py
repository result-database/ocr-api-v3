import requests
import json

import models

def set_data(db):
    music_json = requests.get('https://raw.githubusercontent.com/result-database/ocr-api/main/data/old-music.json')
    difficult_json = requests.get('https://raw.githubusercontent.com/result-database/ocr-api/main/data/old-difficult.json')

    for i in json.loads(music_json.text):
        if (db.query(models.Music).filter(models.Music.id == i['id']).count() == 0):
            db_item = models.Music(
                id=i['id'],
                title=i['title'],
                pronunciation=i['pronunciation'],
                creator=i['creator'],
                lyricist=i['lyricist'],
                composer=i['composer'],
                arranger=i['arranger']
            )
            db.add(db_item)
            db.commit()

    for i in json.loads(difficult_json.text):
        if (db.query(models.Difficult).filter(models.Difficult.id == i['id']).count() == 0):
            db_item = models.Difficult(
                id=i['id'],
                musicId=i['musicId'],
                musicDifficulty=i['musicDifficulty'],
                playLevel=i['playLevel'],
                totalNoteCount=i['totalNoteCount']
            )
            db.add(db_item)
            db.commit()


    return {'ok':True}
