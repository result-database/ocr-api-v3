import json
import requests
from lib.util import load_diff

def getFromOrigin():
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
        
        return { "ok": True, "data": result }
    except:
        return { "ok": False }

def getFromDB(db, models):
    music_db = db.query(models.Music).all()
    tmp = {}
    for m in music_db:
        tmp[m.id] = m
    return { "data": tmp }
    