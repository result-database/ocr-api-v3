import difflib
from lib.util import sort_for_difficult
import time
import json
import requests

def candidateDifficult(target):
    # timer start
    start = time.time()

    difficults = ['EASY', 'NORMAL', 'HARD', 'EXPERT', 'MASTER', 'APPEND']
    datas = []

    for j in difficults:
        result = difflib.SequenceMatcher(None, target, j).ratio()
        datas.append({'credibility': result, 'musicDifficulty': j})

    datas = sort_for_difficult(datas)

    # get time of get-musics-from-db
    time_process = time.time() - start
    start = time.time()

    result = {
        "time": {
            "process": time_process
        },
        "result": datas
    }

    return result

def candidateTitle(target, ratio):
    # timer start
    start = time.time()

    music = json.loads(requests.get("http://localhost:8080/static/music.json").text)

    # get time of get-musics-from-db
    time_query = time.time() - start
    start = time.time()

    datas = []

    for j in music:
        result = difflib.SequenceMatcher(None, target, j["title"].replace(" ", "")).ratio()

        if result > ratio:
            datas.append({'title': j['title'], 'credibility': result, 'musicId': j['id']})

    # get time of do-preprocessing
    time_process = time.time() - start
    start = time.time()

    datas = sort_for_difficult(datas)

    # get time of sort
    time_sort = time.time() - start
    start = time.time()

    result = {
        "ratio": ratio,
        "time": {
            "database": time_query,
            "process": time_process,
            "sort": time_sort
        },
        "result": datas
    }

    return result
