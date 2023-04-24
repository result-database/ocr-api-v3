import difflib
from lib.util import sort_for_difficult
import time

def candidateDifficult(target):
    difficults = ['EASY', 'NORMAL', 'HARD', 'EXPERT', 'MASTER']
    datas = []

    for j in difficults:
        result = difflib.SequenceMatcher(None, target, j).ratio()
        datas.append({'credibility': result, 'musicDifficulty': j})

    datas = sort_for_difficult(datas)

    return datas

def candidateTitle(target, ratio, db, models):
    # timer start
    start = time.time()

    music_db = db.query(models.Music.id, models.Music.title).all()

    # get time of get-musics-from-db
    time_query = time.time() - start
    start = time.time()

    datas = []

    for j in music_db:
        result = difflib.SequenceMatcher(None, target, j[1]).ratio()

        if result > ratio:
            datas.append({'title': j[1], 'credibility': result, 'musicId': j[0]})

    # get time of do-preprocessing
    time_preprocess = time.time() - start
    start = time.time()

    datas = sort_for_difficult(datas)

    # get time of sort
    time_sort = time.time() - start
    start = time.time()

    result = {
        "ratio": ratio,
        "time": {
            "database": time_query,
            "preprocess": time_preprocess,
            "sort": time_sort
        },
        "result": datas
    }

    return result
