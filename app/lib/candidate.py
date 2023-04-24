import difflib
import json
from lib.util import sort_for_difficult
from lib.util import is_float

def candidateDifficult(target):
    difficults = ['EASY', 'NORMAL', 'HARD', 'EXPERT', 'MASTER']
    datas = []

    for j in difficults:
        result = difflib.SequenceMatcher(None, target, j).ratio()
        datas.append({'credibility': result, 'musicDifficulty': j})

    datas = sort_for_difficult(datas)

    return datas

def candidateTitle(target, ratio, music_db):
    # validate border
    # arrow number (else, using 0.5)
    if is_float(ratio):
        ratio = float(ratio)
    else:
        ratio = 0.5

    music = music_db
    datas = []

    for j in music:
        result = difflib.SequenceMatcher(None, target, j[1]).ratio()

        if result > ratio:
            datas.append({'title': j[1], 'credibility': result, 'musicId': j[0]})

    return sort_for_difficult(datas)
