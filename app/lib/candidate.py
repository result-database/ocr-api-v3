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

def candidateTitle(target, ratio):
    # validate border
    # arrow number (else, using 0.5)
    if is_float(ratio):
        ratio = float(ratio)
    else:
        ratio = 0.5

    with open('/app/lib/music.json', encoding='utf-8') as f1:
        music = json.load(f1)
        datas = []

        for j in music:
            result = difflib.SequenceMatcher(None, target, j['title']).ratio()

            if result > ratio:
                datas.append({'title': j['title'], 'credibility': result, 'musicId': j['id']})

        return sort_for_difficult(datas)
